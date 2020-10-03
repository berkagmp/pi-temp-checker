#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define MAXTIMINGS 85
#define DHTPIN 7
int dht11_dat[5] = {0, 0, 0, 0, 0};

int read_dht11_dat()
{
  uint8_t laststate = HIGH;
  uint8_t counter = 0;
  uint8_t j = 0, i;
  float f;

  dht11_dat[0] = dht11_dat[1] = dht11_dat[2] = dht11_dat[3] = dht11_dat[4] = 0;

  pinMode(DHTPIN, OUTPUT);
  digitalWrite(DHTPIN, LOW);
  delay(18);
  digitalWrite(DHTPIN, HIGH);
  delayMicroseconds(40);
  pinMode(DHTPIN, INPUT);

  for (i = 0; i < MAXTIMINGS; i++)
  {
    counter = 0;
    while (digitalRead(DHTPIN) == laststate)
    {
      counter++;
      delayMicroseconds(1);
      if (counter == 255)
      {
        break;
      }
    }
    laststate = digitalRead(DHTPIN);

    if (counter == 255)
      break;

    if ((i >= 4) && (i % 2 == 0))
    {
      dht11_dat[j / 8] <<= 1;
      if (counter > 16)
        dht11_dat[j / 8] |= 1;
      j++;
    }
  }

  if ((j >= 40) &&
      (dht11_dat[4] == ((dht11_dat[0] + dht11_dat[1] + dht11_dat[2] + dht11_dat[3]) & 0xFF)))
  {
    printf("%d.%d/%d.%d", dht11_dat[2], dht11_dat[3], dht11_dat[0], dht11_dat[1]);
    return 1;
  }
  else
  {
    return 0;
  }
}

int main(void)
{
  if (wiringPiSetup() == -1)
    exit(1);

  while (!read_dht11_dat())
  {
    delay(1);
  }

  return (0);
}
