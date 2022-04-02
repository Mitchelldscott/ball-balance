

struct FIFI_Queue
{
	int size;
	int start_idx;
	int current_idx;

	float* array;
};

void insert(FIFO_Queue* queue, float new_value)
{
	// Update the current index
	queue->current_idx += 1;

	// Wrap if too large
	if (queue->current_idx >= queue->size)
		queue->current_idx = 0;

	// Update the start index
	if (queue->current_idx == queue->start_idx)
	{
		queue->start_idx += 1;

		// Wrap if too large
		if (queue->start_idx >= size)
			queue->start_idx = 0;
	}

	queue->array[current_idx] = new_value;
}

float get(FIFO_Queue* queue, int idx)
{
	// Update the index
	idx += queue->start_idx;

	// Wrap if too large
	if (idx >= queue->size)
		idx -= queue->size;

	return queue->array[idx];
}

String toStr(FIFO_Queue* queue)
{
	String s;
	for (int i=0; i < queue->size; i++)
	{
		int idx = queue->start_idx + i;
		if (idx > queue->size)
			idx -= queue->size;

		s += String(queue->array[idx], 4);
	}

	return s;
}



