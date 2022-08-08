import g4p_controls.*;
import processing.serial.*;
//import processing.net.*;

Serial serial;
int BAUDRATE = 9600;

GTextField txf0, txf1, txf2, txf3;
GTextArea ar0;
GButton btn0, btn1;
GDropList drp0; //For buffer IP-adresses

int w=400, h=800;
int area_w = 390, area_h = 200, area_posx = 400, area_posy = 10;
int btn_w = 70, btn_h = 20;


public void setup(){
  size(800, 400);
  
  //Text_zone
  ar0 = new GTextArea(this, area_posx, area_posy, area_w, area_h);
  
  // Message field
  txf0 = new GTextField(this, area_posx, area_posy+5+area_h, area_w-80, 20);
  txf0.tag = "txf0";
  txf0.setPromptText("Enter your message...");
  
  // IP-adress field
  txf1 = new GTextField(this, 20, 40, 150, 20);
  txf1.tag = "txf1";
  txf1.setPromptText("Enter your IP-adress...");
  
  // Port_number
  txf2 = new GTextField(this, 20, 60, 150, 20);
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
  
  //Send_button
  btn0 = new GButton(this, area_posx+area_w-80+10, area_posy+5+area_h, btn_w, btn_h, "Clear");
  btn0.setLocalColorScheme(G4P.RED_SCHEME);
  //Clear_button
  btn1 = new GButton(this, area_posx, area_posy+30+area_h, area_w, btn_h, "Send");
  btn1.setLocalColorScheme(G4P.GREEN_SCHEME);
}

public void draw(){
  background(200, 200, 200);
  
  if (keyPressed == true && (key == ENTER)){
    //serial.write(trim(txf0.getText())+"\n");
    ar0.appendText(millis()/1000.0 + " << "+ txf0.getText());
    delay(200);
  }
}

public void handleButtonEvents(GButton button, GEvent event){
  if(event == GEvent.CLICKED){
    if (button == btn0)
      ar0.setText("");
      //serial.stop();
    if(button == btn1)
      ar0.appendText(millis()/1000.0 + " << "+ txf0.getText());
      //serial.write(txf0.getText()+"\n");
  }
}

public void handleTextEvents(GEditableTextControl textcontrol, GEvent event){
  
}
