#include <SoftwareSerial.h>
SoftwareSerial gps(10,11);

char str[70];
String gpsString="";
char *test="$GPGGA";
String latitude="  ", longitude="   ", key="aawaaraa";
int i, device_id=1;
boolean gps_status=0;
 
void setup(){
  Serial.begin(9600);
  gps.begin(9600);
  gsm_init();
  get_gps();
  delay(500);
}
 
void loop(){
    get_gps();
    tracking();
}
 
void gpsEvent(){
  gpsString="";
  while(!gps_status)
  {
     while (gps.available()>0)            
     {
       char inChar = (char)gps.read();
       gpsString+= inChar;                    
       i++;
       if (i < 7 && gpsString[i-1] != test[i-1]){
          i=0;
          gpsString="";
       }
       if(inChar=='\r')
       if(i>65){
         gps_status=1;
         break;
       }
       else            i=0;
    }
  }
}
 
void get_gps(){
   gps_status=0;
   int x=0;
   while(gps_status==0)
   {
    gpsEvent();
    int str_lenth=i;
    latitude="";
    longitude="";
    int comma=0;
    while(x<str_lenth)
    {
      if(gpsString[x]==',')        comma++;
      if(comma==2)                 latitude+=gpsString[x+1];     
      else if(comma==3)            latitude+=gpsString[x+1];     
      else if(comma==4)            longitude+=gpsString[x+1];
      else if(comma==5)            longitude+=gpsString[x+1];
      x++;
    }
    latitude = latitude.substring(0, latitude.length()-3) + latitude[latitude.length()-2];
    longitude = longitude.substring(0, longitude.length()-3) + longitude[longitude.length()-2];
    i=0;x=0;
    delay(1000);
   }
}
 
void gsm_init(){
  connectGSM("AT","OK");
  connectGSM("ATE0","OK");
  connectGSM("AT+CPIN?","READY");
  connectGSM("AT+CIPSHUT","OK");
  connectGSM("AT+CGATT=1","OK");
  connectGSM("AT+CSTT=\"airtelgprs.com\",\"\",\"\"","OK");
  connectGSM("AT+CIICR","OK");
}
 
void connectGSM (String cmd, char *res){
  while(1){
    Serial.println(cmd);
    delay(500);
    while(Serial.available()>0)
      if(Serial.find(res)){
        delay(1000);
        return;
      }
    delay(500);
  }
}
  
void tracking(){
    connectGSM("AT+CIPSTART=\"TCP\",\"127.0.0.1\",5000", "CONNECT");
    String url = "GET /add?lat=" + latitude + "&long=" + longitude + "&key=" + key + "&id=" + device_id + " HTTP/1.0\r\n\r\n";
    String start = "AT+CIPSEND=";
    start += url.length();
    Serial.println(start);
    Serial.println(url);
    Serial.write(0x1A);
    delay(1000);
}
