
class FIFO_Queue_2D
{
  private:
	  int size;
	  int start_idx;
	  int current_idx;
    float averageX;
    float averageY;
    float array[][2];
  
  public:
    FIFO_Queue_2D();
    FIFO_Queue_2D(int size);
    void insert(float, float);
    float* get(int);
    void print();
    void variance(float*, float*);
};

FIFO_Queue_2D::FIFO_Queue_2D()
{
  size = 50;
  start_idx = 0;
  current_idx = 0;

  averageX = 0.0;
  averageY = 0.0;
}

FIFO_Queue_2D::FIFO_Queue_2D(int s)
{
  size = s;
  start_idx = 0;
  current_idx = 0;

  averageX = 0.0;
  averageY = 0.0;
}

void FIFO_Queue_2D::insert(float x, float y)
{
  // Update the current index
	current_idx += 1;

	// Wrap if too large
	if (current_idx >= size)
		current_idx = 0;

	// Update the start index
	if (current_idx == start_idx)
	{
    averageX -= (array[start_idx][0] / size);
    averageY -= (array[start_idx][1] / size);
		start_idx += 1;

		// Wrap if too large
		if (start_idx >= size)
			start_idx = 0;
	}

	array[current_idx][0] = x;
  array[current_idx][1] = y;
  averageX += (x / size);
  averageY += (y / size);
}

float* FIFO_Queue_2D::get(int idx)
{
	// Update the index
	idx += start_idx;

	// Wrap if too large
	if (idx >= size)
		idx -= size;

	return array[idx];
}

void FIFO_Queue_2D::print()
{
  int length = current_idx - start_idx;
  if (length < 0)
    length = (size - start_idx) + current_idx;

  Serial.print("Queue\n[");

	for (int i=0; i < length; i++)
	{
		int idx = start_idx + i;
		if (idx > size)
			idx -= size;

    Serial.print("(");
    Serial.print(array[idx][0]);
    Serial.print(",");
    Serial.print(array[idx][1]);
    Serial.print(")");

	}
  Serial.println("]\nAverage");
  Serial.print(averageX); Serial.print("\t");
  Serial.println(averageY);

  Serial.println("Variance");
  float varX = 0.0;
  float varY = 0.0;
  variance(&varX, &varY);
  Serial.print(varX); Serial.print("\t");
  Serial.println(varY);
}

void FIFO_Queue_2D::variance(float* varX, float* varY)
{

  int length = current_idx - start_idx;
  if (length < 0)
    length = (size - start_idx) + current_idx;

  for (int i=0; i < length; i++)
	{
		int idx = start_idx + i;
		if (idx > size)
			idx -= size;

    *varX += ((array[idx][0] - averageX) * (array[idx][0] - averageX)) / (length - 1);
    *varY += ((array[idx][1] - averageY) * (array[idx][1] - averageY)) / (length - 1);
  }
}




