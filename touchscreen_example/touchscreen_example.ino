#include "FIFO_Queue.h"

#define P1 A0								// Blue 
#define P2 A1								// Green 
#define P3 A2								// Orange 
#define P4 A3								// Yellow 

// Estimated State
float X;
float Y;

int hx_idx = 0;
int hx0_idx = 0;
int hx_vals = 0;
int hx_size = 50;
float historyX [hx_size];

// Measured values (for each pin)
int X1;
int X2;
int X3;
int X4;

int Y1;
int Y2;
int Y3;
int Y4;

// Noise from pins
int noiseX;
int noiseY;
int noise_tolerance = 20;

// Setup variables for timing handler
unsigned long t;
unsigned long t1;
unsigned long dumprate = 100;

bool is_contact = false;

void dumpState()
{
	/*
	*	Dump the state of the hardware
	* prints position estimate, all measured pins and noise calculation
	* Meant for debug only
	*/

	if (is_contact)
	{
		Serial.println("Axis\tPosition\tMeasurements\t\t\tNoise"); 
		Serial.print("X:\t");
		Serial.print(X); Serial.print("\t\t"); 
		Serial.print(X1); Serial.print("\t");
		Serial.print(X2); Serial.print("\t");
		Serial.print(X3); Serial.print("\t");
		Serial.print(X4); Serial.print("\t");
		Serial.println(float(noiseX)/2048.0);
		Serial.print("Y:\t");
		Serial.print(Y); Serial.print("\t\t");
		Serial.print(Y1); Serial.print("\t");
		Serial.print(Y2); Serial.print("\t");
		Serial.print(Y3); Serial.print("\t");
		Serial.print(Y4); Serial.print("\t");
		Serial.println(float(noiseY)/2048.0);
		Serial.println("---");
	}
	
}

void interval(unsigned long *last_t, unsigned long interval, void (*f)())
{
	t = millis();
	if (t - *last_t > interval)
	{
		*last_t = t;
		f();
	}
}

void setPins(int p1, int p2, int p3, int p4)
{
	pinMode(p1, INPUT);
	pinMode(p2, INPUT);
	digitalWrite(p2, LOW); // Tri-state

	pinMode(p3, OUTPUT);
	digitalWrite(p3, HIGH);

	pinMode(p4, OUTPUT);
	digitalWrite(p4, LOW);
}

void readPins(int *m1, int *m2, int *m3, int *m4, int *noise)
{
	*m1 = analogRead(P1);
	*m2 = analogRead(P2);
	*m3 = analogRead(P3);
	*m4 = analogRead(P4);
	*noise = *m2 + *m4;
}

void updateState()
{
	// Update X first (priority)
	setPins(P1, P2, P3, P4);
	readPins(&X1, &X2, &X3, &X4, &noiseX);
	X = float((X1 - 375) / 525.0) * 100.0;

	// Update Y
	setPins(P3, P4, P1, P2);
	readPins(&Y1, &Y2, &Y3, &Y4, &noiseY);
	Y = float((Y3) / (1024.0)) * 100.0;

	// Update contact
	is_contact = (Y <= 100 && Y >= 0) && (X <= 100 && X >= 0);
}

void new_element(float* array, float new_value, int* current_idx, int* start_idx, int* n_values, int size)
{
	// increment the indices
	current_idx += 1
	if (current_idx >= size)
		current_idx = 0;

	if (current_idx == size)
	{
		*start_idx += 1;
		if (start_idx >= size)
		{
			start_idx = 0;
		}
	}

	// Increment the number of elements
	if (*n_values < size)
	{
		*n_values += 1;
	}

	array[current_idx] = new_value;
}

void history_variance(float* array, int* current_idx,)
{

}

void setup()
{
	Serial.begin(9600);
	t = millis();
	t1 = t;
}

void loop()
{
	interval(&t1, dumprate, &dumpState);
	updateState();
	delay(10);
	
}








