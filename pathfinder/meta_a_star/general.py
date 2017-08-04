# imports
import os
import pickle


# DIRECTORY CHANGES
# meta a* to test data
def m_to_td():
	os.chdir("../")
	os.chdir("data_collection/test_data")
def td_to_m():
	os.chdir("../../")
	os.chdir("meta_a_star")

# GET DATA
def test_data_from_file():
	m_to_td()
	f = open("test_data.p", "rb")
	model_dict = pickle.load(f)
	f.close()
	td_to_m()
	return model_dict