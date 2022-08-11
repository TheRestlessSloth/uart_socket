import g4p_controls.*;
import processing.serial.*;
import processing.net.*;
import java.awt.Font;

                                                                                                   
GTextField ent_message, ent_ip, ent_port, pic_field;                                                // G4P initialization 
GTextArea ar0;
GButton clear_btn, send_btn, pic_but, pic_trans, pic_rec, dcon, ddcon, connect_btn;
GDropList drp_com, drp_baud; //For buffer IP-adresses
GLabel authors, title, con, ip, port, com, baud, pic0, pic1;
GSlider change_mode;

Client mcl;                                                                                         // Client initialization

Serial serial;                                                                                      // Serial initialization

int w=800, h=400;                                                                                   // Position variables 
float area_w = w/2, area_h = h*0.75, area_posx = w/2-10, area_posy = 10;
int btn_w = 70, btn_h = 20;

int ipp_posx = 15, ip_posy = 30;
int p_posy = ip_posy + 25;

boolean sbool = false, host_bool = false;                                                             // Logical variables 

public void setup(){
  size(800, 400);
  
  authors = new GLabel(this, w-w/4, h-30, 200, 20, "(c) By D* Max & Abkerimov T.V.");
  authors.setTextItalic();
  authors.setTextBold();
  
  String[][] titleS = new String[][] {{"UART ----> Socket"}, {"_____Bridge_____"}};
  
  title = new GLabel(this, w/15, h/2-40, 400, 70);
  title.setFont(new Font("Times New Roman", Font.PLAIN, 30));
  title.setText(titleS[0][0]+"\n"+titleS[1][0]);
  title.setTextItalic();
  title.setTextBold();

  //Message zone
  ar0 = new GTextArea(this, area_posx, area_posy, area_w, area_h);

  ent_message = new GTextField(this, area_posx, area_posy+5+area_h, area_w-80, 20);
  ent_message.setPromptText("Enter your message...");
  
  //Send_button
  clear_btn = new GButton(this, area_posx+area_w-80+10, area_posy+5+area_h, btn_w, btn_h, "Clear");
  //Clear_button
  send_btn = new GButton(this, area_posx, area_posy+30+area_h, area_w, btn_h, "Send");
  
  //Connection zone
  con = new GLabel(this, w/2-290, 5, 150, 20, "CONNECTION EDITS"); 
  con.setTextBold();
  ip = new GLabel(this, ipp_posx, ip_posy, 50, 20, "IP: "); 
  ip.setTextBold();
  port = new GLabel(this, ipp_posx, p_posy, 50, 20, "Port: ");
  port.setTextBold();
  
  //IP-adress field
  ent_ip = new GTextField(this, 50, ip_posy, 250, 20);
  ent_ip.setPromptText("Enter your IP-adress...");
  
  //Port number field
  ent_port = new GTextField(this, 50, p_posy, 250, 20);
  ent_port.setPromptText("Number port...");
  
  connect_btn = new GButton(this, ipp_posx, p_posy+25, 250+35, 20, "Connect");
  
  //----------------------------------------COM[i]-------------------------------------------------
  com = new GLabel(this, ipp_posx, ip_posy, 50, 20, "COM: ");
  com.setTextBold();
  
  baud = new GLabel(this, ipp_posx, ip_posy+25, 70, 20, "Baudrate: ");
  baud.setTextBold();
  
  dcon = new GButton(this, 115, ip_posy, 90,20, "Connect");
  ddcon = new GButton(this, 210, ip_posy, 90,20, "Disconnect");

  //String ser_list = "COM3";
  drp_com = new GDropList(this, 50, ip_posy, 60, 90);
  drp_com.addItem(" ");

  String ser_list[] = Serial.list();
  if (ser_list == null){
    ar0.appendText("COM port is not connected!\n");
  }
  else{
    for(int i = 0; i<ser_list.length; i++)
      drp_com.addItem(ser_list[i]);
     drp_com.removeItem(0);
  }
  
  String[] BAUDRATE = new String[] {"300", "1200", "2400", "4800", "9600", 
                                    "19200", "38400", "57600", "74880", "115200",
                                    "230400", "250000", "500000", "1000000", "2000000"}; 
  drp_baud = new GDropList(this, ipp_posx+60, ip_posy+25, 60, 90);
  for(int i=0; i < 15; i++)
    drp_baud.addItem(BAUDRATE[i]);
  drp_baud.setSelected(4);

  String[] ticklabe = new String[] {"C","H"};
  change_mode = new GSlider(this, w/2-80, 15, 40, 40, 10);
  change_mode.setTickLabels(ticklabe);
  change_mode.setShowDecor(false, false, false, true);
  change_mode.setLimits(0, 1);

  //-------------------------------------IMAGE SELECTOR--------------------------------------------
  pic0 = new GLabel(this, w/2-260, h/2+65, 150, 20, "PICTURES PART"); 
  pic0.setTextBold();
  pic1 = new GLabel(this, w/2-395, h/2+90, 50, 20, "Folder: " );
  pic1.setTextBold();
  
  pic_field = new GTextField(this, 50, h/2+90, 250, 20);
  pic_field.setPromptText("");
  
  pic_but = new GButton(this, 55+250, h/2+90, 70, 20, "Browse");
  pic_trans = new GButton(this, 50, h/2+115, 325, 20, "Transmit");
  pic_rec = new GButton(this, 50, h/2 + 140, 325, 20, "Recieve");
}

//------------------------------------------DRAW ZONE----------------------------------------------
public void draw(){
  background(180, 180, 180);
  
  clear_btn.setLocalColorScheme(G4P.RED_SCHEME);
  send_btn.setLocalColorScheme(G4P.GREEN_SCHEME);
  
  dcon.setLocalColorScheme(G4P.GREEN_SCHEME);
  ddcon.setLocalColorScheme(G4P.RED_SCHEME);
  
  pic_but.setLocalColorScheme(G4P.PURPLE_SCHEME);
  pic_trans.setLocalColorScheme(G4P.YELLOW_SCHEME);
  pic_rec.setLocalColorScheme(G4P.GREEN_SCHEME); 

  if ((frameCount % 30 == 0) && sbool)
    thread("requestData");
    
  if ((frameCount % 30 == 0) && host_bool)
    thread("clientRequestData");
}

// ------------------------------------------------------------------------------------------------
void requestData() {
  while (serial.available() > 0)
    ar0.appendText(millis()/1000.0 + " >> "+ serial.readString());   
}
void clientRequestData(){
  if (mcl.available() > 0)
    ar0.appendText(millis()/1000.0 + " >> "+ trim(mcl.readString()));
}

// ----------------------------------HANDLE BUTTONS------------------------------------------------
public void handleButtonEvents(GButton button, GEvent event){
  if(event == GEvent.CLICKED){
    if (button == clear_btn){
      ar0.setText("");
    }
    if(button == send_btn){
      ar0.appendText(millis()/1000.0 + " << "+ ent_message.getText());
      if (sbool)
        serial.write(ent_message.getText()+"\n");
      if (host_bool)
        mcl.write(ent_message.getText()+"\n");
        
      ent_message.setText("");
    }
    if (button == pic_but)
      handleImageSelection(button);
    if (button == pic_trans){
      serial.write(loadBytes((pic_field.getText())));
      ar0.appendText(millis()/1000.0 + " << Picture from: " + pic_field.getText() + " was transmited!");
      delay(200);
    }
    if (button == pic_rec){
      if (mcl.active() == true){
        if(mcl.available()>0){
          ar0.appendText(mcl.readString());
        }
      }
    }
    if (button == dcon){
      serial = new Serial(this, drp_com.getSelectedText(), int(drp_baud.getSelectedText()));
      sbool = true;
      println("Connected to " + drp_com.getSelectedText());
    }
    if (button == ddcon){
      serial.clear();
      serial.stop();
      sbool = false;
      println("Disconnected from " + drp_com.getSelectedText());
    }
    if (button == connect_btn){
      String IP, PORT;
      
      IP = ent_ip.getText();
      PORT = ent_port.getText();
      
      mcl = new Client(this, IP, int(PORT));
      println("Connected with "+ mcl.ip());
      host_bool = true;
    }
  } 
 }


// ----------------------------------HANDLE TEXTS---------------------------------------------------
public void handleTextEvents(GEditableTextControl textcontrol, GEvent event){

  if ((textcontrol == ent_message) && event == GEvent.ENTERED){
    
    ar0.appendText(millis()/1000.0 + " << "+ ent_message.getText());
    
    if(ent_message.getText() == "send"){
      byte[] data = mcl.readBytes();
      saveBytes("Picture.txt", data); // or saveStrings()
  }
      //to do: receive photo, and no display to area, but save to file 
    
    if(sbool)
      serial.write(trim(ent_message.getText())+"\n");
      
    if(host_bool)
      mcl.write(trim(ent_message.getText()+"\n"));
      
    ent_message.setText("");
    delay(200);
  }
}

// ------------------------------------HANDLE FILES-------------------------------------------------
public void handleImageSelection(GButton button){
  String fname;
  
  if(button == pic_but){
    fname = G4P.selectInput("Folder Dialog");
    pic_field.setText(fname);
  }
}

// ------------------------------------HANDLE SLIDER-------------------------------------------------
public void handleSliderEvents(GValueControl slider, GEvent event){
  if(slider == change_mode){
    if (slider.getValueF()==1.0){
      ent_ip.setVisible(true);
      ent_port.setVisible(true);
      ip.setVisible(true);
      port.setVisible(true);
      connect_btn.setVisible(true);
      
      drp_com.setVisible(false);
      drp_baud.setVisible(false);
      dcon.setVisible(false);
      ddcon.setVisible(false);
      com.setVisible(false);
      baud.setVisible(false);
      
      /*
      if (serial != null && event == GEvent.VALUE_STEADY){
        serial.clear();
        serial.stop();
        println("Port disconnected");
      }*/
      sbool = false;
    }
    else {
      ent_ip.setVisible(false);
      ent_port.setVisible(false);
      ip.setVisible(false);
      port.setVisible(false);
      connect_btn.setVisible(false);
      
      drp_com.setVisible(true);
      drp_baud.setVisible(true);
      dcon.setVisible(true);
      ddcon.setVisible(true);
      com.setVisible(true);
      baud.setVisible(true);
     /* 
      if (mcl != null){
        mcl.clear();
        mcl.stop();
        println("Host disconnected");
      }
      */
      host_bool = false;
    }
  }
}
