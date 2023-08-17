#include <Servo.h>

Servo ServoMotor;

//Pino do potenciometro
int pino_pot = A5;
//Pino de controle do motor
int pino_motor = 6;
int valor;

void setup()
{
  Serial.begin(9600);
  ServoMotor.attach(pino_motor);
  Serial.println("Aguardando 5 segundos....");
  delay(5000);
}

void loop()
{
  //Le o valor do potenciometro
  valor = analogRead(pino_pot);
  //Converte o valor para uma faixa entre 0 e 179
  valor = map(valor, 0, 1023, 0, 179);
  //Mostra o valor no serial monitor
  Serial.print("Potenciometro: ");
  Serial.println(valor);
  //Envia o valor para o motor
  ServoMotor.write(valor);
}