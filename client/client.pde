import g4p_controls.*;
import processing.serial.*;
import processing.net.*;
import java.awt.Rectangle;

Client mcl;

Serial serial;
int BAUDRATE = 9600;

GTextField txf0, txf1, txf2, pic_field;
GTextArea ar0;
GButton btn0, btn1, pic_but, pic_trans, pic_rec;
GDropList drp0; //For buffer IP-adresses
GLabel con, ip, port, pic0, pic1;

int w=800, h=400;
float area_w = w/2, area_h = h*0.80, area_posx = w/2-10, area_posy = 10;
int btn_w = 70, btn_h = 20;

int ipp_posx = 15, ip_posy = 30;
int p_posy = ip_posy + 25;

public void setup(){
  size(800, 400);
  
  //Message zone
  ar0 = new GTextArea(this, area_posx, area_posy, area_w, area_h);

  txf0 = new GTextField(this, area_posx, area_posy+5+area_h, area_w-80, 20);
  txf0.tag = "txf0";
  txf0.setPromptText("Enter your message...");
  
  //Send_button
  btn0 = new GButton(this, area_posx+area_w-80+10, area_posy+5+area_h, btn_w, btn_h, "Clear");
  //Clear_button
  btn1 = new GButton(this, area_posx, area_posy+30+area_h, area_w, btn_h, "Send");
  
  //Connection zone
  con = new GLabel(this, w/2-290, 5, 150, 20, "CONNECTION EDITS"); 
  con.setTextBold();
  ip = new GLabel(this, ipp_posx, ip_posy, 50, 20, "IP: "); 
  ip.setTextBold();
  port = new GLabel(this, ipp_posx, p_posy, 50, 20, "Port: ");
  port.setTextBold();
  
  //IP-adress field
  txf1 = new GTextField(this, 50, ip_posy, 250, 20);
  txf1.tag = "txf1";
  txf1.setPromptText("Enter your IP-adress...");
  
  //Port number field
  txf2 = new GTextField(this, 50, p_posy, 250, 20);
  txf2.tag = "txf2";
  txf2.setPromptText("Number port...");
  
  /*
  //Droplist COM[i]
  drp0 = new GDropList(this, 20, 80, 50, 50);
  String ser_list[] = Serial.list();
  if (ser_list == null) {
   print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
   return;
  }
  else {
  for(int i = 0; i<ser_list.length; i++)
    drp0.addItem(ser_list[i]);
  }
  */
  
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
  
  btn0.setLocalColorScheme(G4P.RED_SCHEME);
  btn1.setLocalColorScheme(G4P.GREEN_SCHEME);
  pic_but.setLocalColorScheme(G4P.PURPLE_SCHEME);
  pic_trans.setLocalColorScheme(G4P.YELLOW_SCHEME);
  pic_rec.setLocalColorScheme(G4P.GREEN_SCHEME);
  
}
// ----------------------------------HANDLE BUTTONS------------------------------------------------
public void handleButtonEvents(GButton button, GEvent event){
  if(event == GEvent.CLICKED){
    if (button == btn0)
      ar0.setText("");
      //serial.stop();
    if(button == btn1)
      ar0.appendText(millis()/1000.0 + " << "+ txf0.getText());
      //serial.write(txf0.getText()+"\n");
    if (button == pic_but)
      handleFileDialog(button);
    if (button == pic_trans){
      //serial.write(pic_field.getText()+"\n");
      ar0.appendText(millis()/1000.0 + " << Picture from: " + pic_field.getText() + " was transmited!");
      delay(200);
    }
    if (button == pic_rec){
      //mcl.read();
    }
  }
}
// ----------------------------------HANDLE TEXTS---------------------------------------------------
public void handleTextEvents(GEditableTextControl textcontrol, GEvent event){
  String IP, PORT;
  
  if ((textcontrol == txf0) && keyPressed == true && (key == ENTER)){
    //serial.write(trim(txf0.getText())+"\n");
    ar0.appendText(millis()/1000.0 + " << "+ txf0.getText());
    delay(200);
  }
  if((textcontrol == txf1) && keyPressed == true && (key == ENTER)){
        IP = txf1.getText();
         if((textcontrol == txf2) && keyPressed == true && (key == ENTER)){
             PORT = txf2.getText();
             mcl = new Client(this, IP, int(PORT));
         }
  }
}

public void handleFileDialog(GButton button){
  String fname;
  
  if(button == pic_but){
    fname = G4P.selectFolder("Folder Dialog");
    pic_field.setText(fname);
  }
}
