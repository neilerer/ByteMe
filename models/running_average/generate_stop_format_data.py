# imports
import change_directories
import get_file_names
import source_data



def get_jpi_names():
	change_directories.to_jpi()
	jpi_names = get_file_names.all_csv()
	change_directories.from_jpi()
	return jpi_names



jpi_names = get_jpi_names()
for jpi in jpi_names:
	change_directories.to_jpi()
	jpi_data = source_data.open_jpi(jpi)
	jpi_data.close()
	change_directories.from_jpi()
	print(jpi)
