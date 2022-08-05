import processing.serial.*;
import g4p_controls.*;

int BAUDRATE = 9600;
int w = 400, h = 200;
int bw = 40, bh = 20, off = 10;

Serial serial;
GButton btn0, btn1, btn2;
GDropList dlist;
GTextArea text;

public void setup(){
  size(400,200);
  
  btn0 = new GButton(this, off, h/2-bh-off, bw, bh, "Att");
  btn0.setLocalColorScheme(G4P.GREEN_SCHEME);
  
  btn1 = new GButton(this, off, h/2, bw, bh, "Det");
  btn1.setLocalColorScheme(G4P.RED_SCHEME);
  
  btn2 = new GButton(this, 3*off+2*bw, h/2-bh/2, bw, bh, "trans");
  btn2.setLocalColorScheme(G4P.YELLOW_SCHEME);
  
  dlist = new GDropList(this, 50, 50, 50, 50);
  String ser_list[] = Serial.list();
  for(int i = 0; i<ser_list.length;i++)
    dlist.addItem(ser_list[i]);
  
  text = new GTextArea(this,180,30,150,120);
  text.setFocus(true);
  
}

public void draw(){
  background(240);
  if(keyPressed && key == ENTER)
  {
      print(text.getText());
      text.setText("");
  }
}

/**
 * Click the button to create the windows.
 * @param button
 */
public void handleButtonEvents(GButton button, GEvent event) {
  if (event == GEvent.CLICKED) 
  {
    if(button == btn0){
      serial = new Serial(this, dlist.getSelectedText(),BAUDRATE);
      print(dlist.getSelectedText());
    }
    
    if(button == btn1)
      serial.stop();
    
    if(button == btn2)
      serial.write("HAAAAAAAAAAAAAAAAAAAAAAAAAA!");
  }
}
