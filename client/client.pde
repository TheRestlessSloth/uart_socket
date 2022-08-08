import processing.serial.*;
import g4p_controls.*;

int BAUDRATE = 9600;
int w = 400, h = 200;
int bw = 40, bh = 20, off = 10;

Serial serial;
GButton btn0, btn1, btn2;
GDropList dlist;
GTextArea text;
GTextField text2;

public void setup(){
  size(400,200);
  
  btn0 = new GButton(this, off, off+bh, bw, bh, "Att");
  btn0.setLocalColorScheme(G4P.GREEN_SCHEME);
  
  btn1 = new GButton(this, off+bw, off+bh, bw, bh, "Det");
  btn1.setLocalColorScheme(G4P.RED_SCHEME);
  
  btn2 = new GButton(this, 3*off+2*bw, h/2-bh/2, bw, bh, "trans");
  btn2.setLocalColorScheme(G4P.YELLOW_SCHEME);
  
  dlist = new GDropList(this, off, off, bw*2, bh*4);
  String ser_list[] = Serial.list();
  for(int i = 0; i<ser_list.length;i++)
    dlist.addItem(ser_list[i]);
  
  text = new GTextArea(this,180,30,150,120);
  text.setFocus(true);
  
  text2 = new GTextField(this,180,180,150,70);
  text2.setFocus(true);
  
}

public void draw(){
  background(240);
    if(keyPressed && key == ENTER)
    {
      serial.write(trim(text.getText())+"\n");
      text.setText("");
      delay(200);
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
