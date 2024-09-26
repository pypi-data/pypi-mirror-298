class MetricsCalculate:
    def calculate_redudancy(self, data):
        """ Calculate redudancy dari besarnya ukuran sebelum dan setelah removing duplicate"""
        initial_size = len(data)
        transformed_data = DataTransform().remove_duplicates(data)
        final_size = len(transformed_data)
        redudancy_percentage = (initial_size - final_size) / initial_size * 100
        return redudancy_percentage