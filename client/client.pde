import g4p_controls.*;
import processing.serial.*;
import processing.net.*;
import java.awt.Font;

                                                                                                   
GTextField ent_message, ent_ip, ent_port, pic_field;                                                // G4P initialization 
GTextArea ar_mes, ar_cons;
GButton clear_btn, send_btn, pic_but, pic_trans, pic_rec, dcon, ddcon, connect_btn, disconnect_btn;
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

boolean sbool = false, host_bool = false, cringe = false;                                                             // Logical variables 

public void setup(){
  size(800, 400);

  //-------------------------------------MESSAGES ZONE---------------------------------------------
  ar_mes = new GTextArea(this, area_posx, area_posy, area_w, area_h/1.5);

  ent_message = new GTextField(this, area_posx, area_posy+5+area_h/1.5, area_w-80, 20);
  ent_message.setPromptText("Enter your message...");
  
  //Send_button
  clear_btn = new GButton(this, area_posx+area_w-80+10, area_posy+5+area_h/1.5, btn_w, btn_h, "Clear");
  //Clear_button
  send_btn = new GButton(this, area_posx, area_posy+30+area_h/1.5, area_w, btn_h, "Send");
  
  //-------------------------------------CONSOLE---------------------------------------------------
  ar_cons = new GTextArea(this, area_posx, h/2+h/6, area_w, area_h/3);
  
  //-----------------------------------CONNECTION ZONE---------------------------------------------
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
  disconnect_btn = new GButton(this, ipp_posx, p_posy+45, 250+35, 20, "Disconnect");
  
  //----------------------------------------COM[i]-------------------------------------------------
  com = new GLabel(this, ipp_posx, ip_posy, 50, 20, "COM: ");
  com.setTextBold();
  
  baud = new GLabel(this, ipp_posx, ip_posy+25, 70, 20, "Baudrate: ");
  baud.setTextBold();
  
  dcon = new GButton(this, 115, ip_posy, 90,20, "Connect");
  ddcon = new GButton(this, 210, ip_posy, 90,20, "Disconnect");

  //String ser_list = "COM3";
  drp_com = new GDropList(this, 50, ip_posy+1, 60, 90);
  drp_com.addItem(" ");

  String ser_list[] = Serial.list();
  if (ser_list == null){
    ar_mes.appendText("COM port is not connected!\n");
  }
  else{
    for(int i = 0; i<ser_list.length; i++)
      drp_com.addItem(ser_list[i]);
     drp_com.removeItem(0);
  }
  
  String[] BAUDRATE = new String[] {"300", "1200", "2400", "4800", "9600", 
                                    "19200", "38400", "57600", "74880", "115200",
                                    "230400", "250000", "500000", "1000000", "2000000"}; 
  drp_baud = new GDropList(this, ipp_posx+60, ip_posy+26, 60, 90);
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
  
  //--------------------------------------AUTHORS--------------------------------------------------
  authors = new GLabel(this, w-w/4, h-30, 200, 20, "(c) By D* Max & Abkerimov T.V.");
  authors.setTextItalic();
  authors.setTextBold();
  
  String[][] titleS = new String[][] {{"UART ----> Socket"}, {"_____Bridge_____"}};
  
  title = new GLabel(this, w/15, h/2-40, 400, 70);
  title.setFont(new Font("Times New Roman", Font.PLAIN, 30));
  title.setText(titleS[0][0]+"\n"+titleS[1][0]);
  title.setTextItalic();
  title.setTextBold();
}

//---------------------------------------DRAW ZONE-------------------------------------------------
public void draw(){
  background(150, 150, 150);
  
  clear_btn.setLocalColorScheme(G4P.RED_SCHEME);
  send_btn.setLocalColorScheme(G4P.GREEN_SCHEME);
  
  dcon.setLocalColorScheme(G4P.GREEN_SCHEME);
  ddcon.setLocalColorScheme(G4P.RED_SCHEME);
  
  pic_but.setLocalColorScheme(G4P.PURPLE_SCHEME);
  pic_trans.setLocalColorScheme(G4P.YELLOW_SCHEME);
  pic_rec.setLocalColorScheme(G4P.GREEN_SCHEME); 
  
  drp_com.setLocalColor(5, color(150, 150, 150));
  drp_com.setLocalColor(6, color(150, 150, 150));
  drp_baud.setLocalColor(5, color(150, 150, 150));
  drp_baud.setLocalColor(6, color(150, 150, 150));

  ar_mes.setLocalColor(7, color(220, 220, 220));
  ar_mes.setLocalColor(6, color(100, 100, 100));
  ar_mes.setLocalColor(2, color(0, 0, 0));
  
  ar_cons.setLocalColor(7, color(220, 220, 220));
  ar_cons.setLocalColor(6, color(100, 100, 100));
  ar_cons.setLocalColor(2, color(0, 0, 0));
  
  if ((frameCount % 30 == 0) && sbool)
    thread("requestData");
    
  if ((frameCount % 30 == 0) && host_bool)
    thread("clientRequestData");
}

// -----------------------------------DATA REQUESTS------------------------------------------------
void requestData() {
  while (serial.available() > 0){
     //ar_mes.appendText(millis()/1000.0 + " >> "+ serial.readString());
     if (cringe){
       ar_mes.appendText(ar_mes.getText());
       byte[] data = serial.readBytes();
       saveBytes("Picture.png", data); // or saveStrings()
     } 
  }  
}
void clientRequestData(){
  if (mcl.available() > 0)
    ar_mes.appendText(millis()/1000.0 + " >> "+ trim(mcl.readString()));
}

// ----------------------------------HANDLE BUTTONS------------------------------------------------
public void handleButtonEvents(GButton button, GEvent event){
  if(event == GEvent.CLICKED){
    if (button == clear_btn){
      ar_mes.setText("");
    }
    if(button == send_btn){
      ar_mes.appendText(millis()/1000.0 + " << "+ ent_message.getText());
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
      ar_mes.appendText(millis()/1000.0 + " << Picture from: " + pic_field.getText() + " was transmited!");
      delay(200);
    }
    if (button == pic_rec){
      if (mcl.active() == true){
        if(mcl.available()>0){
          ar_mes.appendText(mcl.readString());
        }
      }
    }
    if (button == dcon){
      serial = new Serial(this, drp_com.getSelectedText(), int(drp_baud.getSelectedText()));
      sbool = true;
      ar_cons.appendText("Connected to " + drp_com.getSelectedText());
    }
    if (button == ddcon){
      serial.clear();
      serial.stop();
      sbool = false;
      ar_cons.appendText("Disconnected from " + drp_com.getSelectedText());
    }
    if (button == connect_btn){
      String IP, PORT;
      
      IP = ent_ip.getText();
      PORT = ent_port.getText();
      
      mcl = new Client(this, IP, int(PORT));
      ar_cons.appendText("Connected with "+ mcl.ip());
      host_bool = true;
    }
    if (button == disconnect_btn){      
      try{
        mcl.clear();
        mcl.stop();
        ar_cons.appendText("PORT DISCONNECTED");
      } 
      catch (Exception e){
          //ar_cons.appendText("Port already close!");
      }
      host_bool = false;
    }
  } 
 }

// ----------------------------------HANDLE TEXTS---------------------------------------------------
public void handleTextEvents(GEditableTextControl textcontrol, GEvent event){

  if ((textcontrol == ent_message) && event == GEvent.ENTERED){
    ar_mes.appendText(millis()/1000.0 + " << "+ ent_message.getText());
    cringe = true;
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
      disconnect_btn.setVisible(true);
      
      drp_com.setVisible(false);
      drp_baud.setVisible(false);
      dcon.setVisible(false);
      ddcon.setVisible(false);
      com.setVisible(false);
      baud.setVisible(false);

      if (event == GEvent.VALUE_STEADY){
        try{
          serial.clear();
          serial.stop();
          ar_cons.appendText("PORT DISCONNECTED");
        } 
        catch (Exception e){
          //ar_cons.appendText("Port already close!");
        }
        sbool = false;
      }
    }
    else {
      ent_ip.setVisible(false);
      ent_port.setVisible(false);
      ip.setVisible(false);
      port.setVisible(false);
      connect_btn.setVisible(false);
      disconnect_btn.setVisible(false);
      
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
        ar_cons.appendText("Host disconnected");
      }
      */
      if (event == GEvent.VALUE_STEADY){
       try{
         mcl.clear();
         mcl.stop();
         ar_cons.appendText("CLIENT DISCONNECTED");
        } 
        catch (Exception e){
          //ar_cons.appendText("Port already close!");
        }
        host_bool = false;
      }
    }
  }
}
