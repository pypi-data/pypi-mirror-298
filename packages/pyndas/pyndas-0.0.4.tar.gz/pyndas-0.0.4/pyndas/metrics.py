import time

class MetricsCalculate:
    def calculate_redundancy(self, data):
        """
        Calculate redundancy from the size before and after removing duplicates.
        Also, measure the time taken for the transformation process.
        """
        # Measure initial size
        initial_size = len(data)

        # Start timing
        start_time = time.time()

        # Perform transformation: removing duplicates
        transformed_data = DataTransform().remove_duplicates(data)

        # Stop timing
        elapsed_time = time.time() - start_time

        # Measure final size
        final_size = len(transformed_data)

        # Calculate redundancy percentage
        redundancy_percentage = (initial_size - final_size) / initial_size * 100

        return {
            "redundancy_percentage": redundancy_percentage,
            "elapsed_time": elapsed_time,
        }

    def calculate_transformation_time(self, data):
        """
        Calculate the time taken to flatten and deduplicate nested data.
        """
        # Start timing
        start_time = time.time()

        # Perform the data transformation: flattening + removing duplicates
        data_transform = DataTransform()
        flattened_data = data_transform.flatten_data(data)
        unique_data = data_transform.remove_duplicates(flattened_data)

        # Stop timing
        elapsed_time = time.time() - start_time

        return {
            "flattened_data": flattened_data,
            "unique_data": unique_data,
            "elapsed_time": elapsed_time
        }
