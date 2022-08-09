import g4p_controls.*;
import processing.serial.*;
import processing.net.*;

Client mcl;

Serial serial;
int BAUDRATE = 9600;

GTextField ent_message, ent_ip, ent_port, pic_field;
GTextArea ar0;
GButton clear_btn, send_btn, pic_but, pic_trans, pic_rec, dcon, ddcon, connect_btn;
GDropList drp0; //For buffer IP-adresses
GLabel con, ip, port, com, pic0, pic1;

int w=800, h=400;
float area_w = w/2, area_h = h*0.80, area_posx = w/2-10, area_posy = 10;
int btn_w = 70, btn_h = 20;

int ipp_posx = 15, ip_posy = 30;
int p_posy = ip_posy + 25;

boolean sbool = false;

public void setup(){
  size(800, 400);
  
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
  com = new GLabel(this, ipp_posx, p_posy+25, 50, 20, "COM: ");
  com.setTextBold();
  
  //IP-adress field
  ent_ip = new GTextField(this, 50, ip_posy, 250, 20);
  ent_ip.setPromptText("Enter your IP-adress...");
  
  //Port number field
  ent_port = new GTextField(this, 50, p_posy, 250, 20);
  ent_port.setPromptText("Number port...");
  
  connect_btn = new GButton(this, 50, 200, 50, 20, "INd");
  
  //COM[i]
  dcon = new GButton(this, 115, p_posy+25, 60,20, "Connect");
  ddcon = new GButton(this, 180, p_posy+25, 70,20, "Disconnect");

  //String ser_list = "COM3";
  drp0 = new GDropList(this, 50, p_posy+25, 60, 90);
  drp0.addItem(" ");

  String ser_list[] = Serial.list();
  if (ser_list == null){
    println("COM port is not connected!");
  }
  else{
    drp0.removeItem(0);
    for(int i = 0; i<ser_list.length; i++)
      drp0.addItem(ser_list[i]);
  }

  //File system
  pic0 = new GLabel(this, w/2-280, h/2, 150, 20, "PICTURES PART"); 
  pic0.setTextBold();
  pic1 = new GLabel(this, w/2-395, h/2+30, 50, 20, "Folder: " );
  pic1.setTextBold();
  
  pic_field = new GTextField(this, 50, h/2+30, 250, 20);
  pic_field.setPromptText("");
  
  pic_but = new GButton(this, 55+250, h/2+30, 70, 20, "Browse");
  pic_trans = new GButton(this, 50, h/2+55, 325, 20, "Transmit");
  pic_rec = new GButton(this, 50, h/2 + 80, 325, 20, "Recieved");
}

// ----------------------------------DRAW ZONE-----------------------------------------------------
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
}

void requestData() {
  while (serial.available() > 0)
    ar0.appendText(millis()/1000.0 + " << "+ serial.readString());
}

// ----------------------------------HANDLE BUTTONS------------------------------------------------
public void handleButtonEvents(GButton button, GEvent event){
  if(event == GEvent.CLICKED){
    if (button == clear_btn){
      ar0.setText("");
    }
    if(button == send_btn){
      ar0.appendText(millis()/1000.0 + " << "+ ent_message.getText());
      serial.write(ent_message.getText()+"\n");
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
      serial = new Serial(this, drp0.getSelectedText(), BAUDRATE);
      sbool = true;
      println(drp0.getSelectedText());
    }
    if (button == ddcon){
      serial.clear();
      serial.stop();
      sbool = false;
    }
    if (button == connect_btn){
      String IP, PORT;
      IP = ent_ip.getText();
        PORT = ent_port.getText();
        mcl = new Client(this, IP, int(PORT));
        println("Connected with "+ mcl.ip());
    }
  } 
 }


// ----------------------------------HANDLE TEXTS---------------------------------------------------
public void handleTextEvents(GEditableTextControl textcontrol, GEvent event){

  if ((textcontrol == ent_message) && event == GEvent.ENTERED){
    //serial.write(trim(ent_message.getText())+"\n");
    mcl.write(trim(ent_message.getText()+"\n"));
    ar0.appendText(millis()/1000.0 + " << "+ ent_message.getText());
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
