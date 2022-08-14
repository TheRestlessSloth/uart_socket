import g4p_controls.*;
import processing.serial.*;
import processing.net.*;
import java.awt.Font;


int w=800, h=400;                                                                                   // Position variables 
float area_w = w/2, area_h = h*0.75, area_posx = w/2-10, area_posy = 10;
int btn_w = 70, btn_h = 20;

int ipp_posx = 15, ip_posy = 30;
int p_posy = ip_posy + 25;

boolean sbool = false, host_bool = false;    


GTextField ent_message, pic_field;                                                                  // G4P initialization 
GTextField ent_ip, ent_port;

GTextField ipProfileField;
GTextArea ipProfileArea;

GTextArea ar_mes, ar_cons;

GButton clear_btn, send_btn;
GButton pic_but, pic_trans, pic_rec; 
GButton port_con, port_dcon, ip_con, ip_dcon;
GButton ipProfileSave, ipProfileLoad, ipProfileDel;

GDropList drp_com, drp_baud; //For buffer IP-adresses
GLabel authors, title, con, ip, port, com, baud, pic0, pic1;
GSlider change_mode;

Client mcl;                                                                                         // Client initialization

Serial serial;                                                                                      // Serial initialization
 

//----------------------------------------SETUP----------------------------------------------------
public void setup(){
  size(800, 400);

  setAreaMessage();  
  ar_cons = new GTextArea(this, area_posx, h/2+h/6, area_w, area_h/3); // Console
  setConnectionZone();
  ipProfileSaver();
  changerFunct();
  comPortsSet();
  imageSelector();
  titleFunct();
}

//---------------------------------------DRAW ZONE-------------------------------------------------
public void draw(){
  background(150, 150, 150);
  
  clear_btn.setLocalColorScheme(G4P.RED_SCHEME);
  send_btn.setLocalColorScheme(G4P.GREEN_SCHEME);
  
  port_con.setLocalColorScheme(G4P.GREEN_SCHEME);
  port_dcon.setLocalColorScheme(G4P.RED_SCHEME);
  
  ipProfileArea.setLocalColor(7, color(220, 220, 220));
  ipProfileArea.setLocalColor(6, color(100, 100, 100));
  ipProfileArea.setLocalColor(2, color(0, 0, 0));
  
  ipProfileSave.setLocalColorScheme(G4P.GREEN_SCHEME);
  ipProfileDel.setLocalColorScheme(G4P.RED_SCHEME);
  
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
} //<>//


void setAreaMessage(){
  ar_mes = new GTextArea(this, area_posx, area_posy, area_w, area_h/1.5);

  ent_message = new GTextField(this, area_posx, area_posy+5+area_h/1.5, area_w-80, 20);
  ent_message.setPromptText("Enter your message...");
  
  //Send_button
  clear_btn = new GButton(this, area_posx+area_w-80+10, area_posy+5+area_h/1.5, btn_w, btn_h, "Clear");
  //Clear_button
  send_btn = new GButton(this, area_posx, area_posy+30+area_h/1.5, area_w, btn_h, "Send");
}

void setConnectionZone(){
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
  
  ip_con = new GButton(this, ipp_posx, p_posy+25, 250+35, 20, "Connect");
  ip_dcon = new GButton(this, ipp_posx, p_posy+45, 250+35, 20, "Disconnect");
}

void ipProfileSaver(){
  ipProfileArea = new GTextArea(this, ipp_posx, p_posy+105, 285, 100);
  
  fileWork();
  
  ipProfileField = new GTextField(this, ipp_posx, p_posy+80, 285, 20);
  ipProfileField.setPromptText("Enter your profile name...");
  
  ipProfileSave = new GButton(this, ipp_posx+300, p_posy+80, 60, 35, "Save profile");
  ipProfileLoad = new GButton(this, ipp_posx+300, p_posy+120, 60, 35, "Load profile");
  ipProfileDel = new GButton(this, ipp_posx+300, p_posy+160, 60, 35, "Delete profile");
  
}

void fileWork(){
  File dir = new File("E:/Games/Learning/Proceesing_Proj/client/");
  
  String[] pathnames;
  pathnames = dir.list();
  
  for (String pathname : pathnames){
    if (pathname.endsWith(".conf"))
      ipProfileArea.appendText(pathname);
  }
}

void comPortsSet(){
  com = new GLabel(this, ipp_posx, ip_posy, 50, 20, "COM: ");
  com.setTextBold();
  
  baud = new GLabel(this, ipp_posx, ip_posy+25, 70, 20, "Baudrate: ");
  baud.setTextBold();
  
  port_con = new GButton(this, 115, ip_posy, 90,20, "Connect");
  port_dcon = new GButton(this, 210, ip_posy, 90,20, "Disconnect");

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

}

void changerFunct(){
  String[] ticklabe = new String[] {"S","C"};
  change_mode = new GSlider(this, w/2-80, 15, 40, 40, 10);
  change_mode.setTickLabels(ticklabe);
  change_mode.setShowDecor(false, false, false, true);
  change_mode.setLimits(0, 1);
}

void imageSelector(){
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

void titleFunct(){
  authors = new GLabel(this, w-w/4, h-30, 200, 20, "(c) By D* Max & Abkerimov T.V.");
  authors.setTextItalic();
  authors.setTextBold();
  
  String[][] titleS = new String[][] {{"UART --> Socket"}, {" Bridge"}};
  
  title = new GLabel(this, w/50, h-30, 400, 20);
  title.setFont(new Font("Times New Roman", Font.PLAIN, 16));
  title.setText(titleS[0][0]+titleS[1][0]);
  title.setTextItalic();
  title.setTextBold();
}

void ipConnection (String IP, String PORT, boolean stat){
  if (stat){
    mcl = new Client(this, IP, int(PORT));
    ar_cons.appendText("Connected with "+ mcl.ip());
  }
  else {
    mcl.clear();
    mcl.stop();
    ar_cons.appendText("Disconnected");
  }
  host_bool = stat;
}

void comPortConnection(String comName,int baudrate, boolean stat){
  if (stat){
    serial = new Serial(this, comName, baudrate);
    ar_cons.appendText("Connected to " + drp_com.getSelectedText());
  }
  else {
    serial.clear();
    serial.stop();
    ar_cons.appendText("Disconnected from " + drp_com.getSelectedText());
  } 
  sbool = stat;
}

void visibleSet(boolean isVis){
      ent_ip.setVisible(isVis);
      ent_port.setVisible(isVis);
      ip.setVisible(isVis);
      port.setVisible(isVis);
      ip_con.setVisible(isVis);
      ip_dcon.setVisible(isVis);
      
      ipProfileArea.setVisible(isVis);
      ipProfileField.setVisible(isVis);
      ipProfileArea.setVisible(isVis);
      ipProfileSave.setVisible(isVis);
      ipProfileLoad.setVisible(isVis);
      ipProfileDel.setVisible(isVis);
      
      drp_com.setVisible(!isVis);
      drp_baud.setVisible(!isVis);
      port_con.setVisible(!isVis);
      port_dcon.setVisible(!isVis);
      com.setVisible(!isVis);
      baud.setVisible(!isVis);
}

void requestData() {
  while (serial.available() > 0){
    ar_mes.appendText(millis()/1000.0 + " >> " + serial.readString());
    if ((serial.readString()).equals("preambl"))
      thread("requestImage();");
  }
}

void requestImage(){
  while (serial.available() > 0){
    byte[] dataB = serial.readBytes();
    saveBytes("Picture.png", dataB);
  }
}

void clientRequestData(){
  if (mcl.available() > 0)
    ar_mes.appendText(millis()/1000.0 + " >> "+ trim(mcl.readString()));
}

void commands(String command) {
  /*
  switch (trim(command)){
    case "send":
      status = 1;
    case "dzihurda":
      status = 0;
*/
}

// ----------------------------------HANDLE TEXTS---------------------------------------------------
public void handleTextEvents(GEditableTextControl textcontrol, GEvent event){

  if ((textcontrol == ent_message) && event == GEvent.ENTERED){
    ar_mes.appendText(millis()/1000.0 + " << "+ ent_message.getText());

    if(sbool)
      serial.write(trim(ent_message.getText())+"\n");
      
    if(host_bool)
      mcl.write(trim(ent_message.getText()+"\n"));
   
    ent_message.setText("");
    delay(200);
  }
  if ((textcontrol == ipProfileArea) && event == GEvent.CLICKED){
    ipProfileArea.getSelectedText();
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
      visibleSet(true);
      
      if (event == GEvent.VALUE_STEADY){
        try{
          comPortConnection(drp_com.getSelectedText(), int(drp_baud.getSelectedText()), false);
        } 
        catch (Exception e){}
      }
    }
    else {
      visibleSet(false);
      
      if (event == GEvent.VALUE_STEADY){
       try{
         ipConnection(ent_ip.getText(), ent_port.getText(), false);
       } 
       catch (Exception e){}
      }
    }
  }
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
      pic_field.setText("");
      delay(200);
    }
    
    if (button == pic_rec){
      if (mcl.active() == true){
        if(mcl.available()>0){
          ar_mes.appendText(mcl.readString());
        }
      }
    }
    
    if (button == port_con){
      comPortConnection(drp_com.getSelectedText(), int(drp_baud.getSelectedText()), true);
    }
    
    if (button == port_dcon){
      comPortConnection(drp_com.getSelectedText(), int(drp_baud.getSelectedText()), false);
    }
    
    if (button == ip_con){
      ipConnection(ent_ip.getText(), ent_port.getText(), true);
    }
    
    if (button == ip_dcon){      
      try{
        ipConnection(ent_ip.getText(), ent_port.getText(), false);
      } 
      catch (Exception e){}
    }
    
    if (button == ipProfileSave){ 
      String[] conDat = new String[] {ent_ip.getText(), ent_port.getText()};
      
      saveStrings(ipProfileField.getText()+".conf", conDat);
      
      ipProfileArea.appendText(ipProfileField.getText()+".conf");
      ipProfileField.setText("");
    }
    if (button == ipProfileLoad){
      String[] linesData = loadStrings("E:/Games/Learning/Proceesing_Proj/client/"+ipProfileArea.getSelectedText());
      
      ent_ip.setText(linesData[0]);
      ent_port.setText(linesData[1]);
    }
    if (button == ipProfileDel){
      File needProf = new File("E:/Games/Learning/Proceesing_Proj/client/"+ipProfileArea.getSelectedText());
      needProf.delete();
      ipProfileArea.setText("");
      fileWork();
    }
  }
 }
