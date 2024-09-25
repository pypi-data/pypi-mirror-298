import sys
sys.path.append(".")
import unittest
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
from src.susie.timing_data import TimingData
from .helpers import assertDictAlmostEqual
from src.susie.ephemeris import Ephemeris, LinearModelEphemeris, QuadraticModelEphemeris, PrecessionModelEphemeris, ModelEphemerisFactory

test_epochs = np.array([0, 294, 298, 573])
test_mtts = np.array([2454515.525,2454836.403,2454840.769,2455140.91])
test_mtts_err = np.array([0.00043, 0.00028, 0.00062, 0.00042])
test_tra_or_occ = np.array(['tra','occ','tra','occ'])
test_tra_or_occ_enum = [0 if i == 'tra' else 1 for i in test_tra_or_occ]

test_P_fits = 1.091423

test_P_linear =  1.0904734088754364 # period linear
test_P_err_linear =  0.0006807481006299065 # period error linear
test_T0_linear =2454515.423966982# conjunction time
test_T0_err_linear = 0.23692092991744518  # conjunction time error

test_P_quad =  1.0892663209112947#period quad
test_P_err_quad =  0.002368690041166098 # period err quad
test_T0_quad = 2454515.5241231285 #conjunction time quad
test_T0_err_quad = 0.3467430587812461#conjunction time err quad
test_dPdE =  4.223712653342504e-06#period change by epoch
test_dPdE_err = 7.742732700893123e-06#period change by epoch error

test_epochs_precession = np.array([ -1640, -1346,  -1342, -1067, -1061, -1046,  -1038])
test_mtts_precession = np.array([2454515.525,2454836.403,2454840.769,2455140.91, 2455147.459, 2455163.831,2455172.561])
test_mtts_err_precession = np.array([0.00043, 0.00028, 0.00062, 0.00042, 0.00043, 0.00032, 0.00036])
test_tra_or_occ_precession = np.array(['tra','occ','occ','tra', 'tra', 'tra', 'tra'])
test_tra_or_occ_enum_precession = [0 if i == 'tra' else 1 for i in test_tra_or_occ_precession]
test_P_pre =  1.0914233780823739
test_P_err_pre =  2.5837552101593316e-06
test_T0_pre =  2454515.5247473116
test_T0_err_pre =  0.0016189004920040013
test_dwdE =  -862310.36579702
test_dwdE_err = 1933.7369753292073
test_e =  0.5345414535549522
test_e_err = 13588.186664524692
test_w =  -55020653.47561098
test_w_err= 589049.1819169023

test_observed_data = test_mtts
test_uncertainties= test_mtts_err    


class TestLinearModelEphemeris(unittest.TestCase):
    def setUp(self):
        self.ephemeris = LinearModelEphemeris()

    def test_lin_model_instantiation(self):
        # Tests that ephemeris is an instance of LinearModelEphemeris
        self.assertIsInstance(self.ephemeris, LinearModelEphemeris)
   
    def test_lin_fit(self):
        """Tests that the lin_fit function works.

            Creates a numpy.ndarray[int] with the length of the test data.
            NOTE: The last number should round to 626
        """
        T0 = 0
        expected_result = np.array([  0. ,321.4240735, 325.244054,  625.9310905])
        result = self.ephemeris.lin_fit(test_epochs, test_P_fits, T0, test_tra_or_occ_enum)
        print(result)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))

    def test_lin_fit_model(self):
        """Testing that the dictionary parameters of fit model are equal to what they are suppose to be

            Tests the creation of a dictionary named return_data containing the linear fit model data in the order of:
            {'period': float,
            'period_err': float,
            'conjunction_time': float,
            'conjunction_time_err':float}    
        """
        result = self.ephemeris.fit_model(test_epochs, test_mtts, test_mtts_err, test_tra_or_occ)
        return_data = {
            'period': 1.0904734088754364,
            'period_err': 0.0006807481006299065,
            'conjunction_time': 2454515.423966982 ,
            'conjunction_time_err': 0.23692092991744518 
        }
        self.assertEqual(result['period'], return_data['period'])
        self.assertEqual(result['period_err'], return_data['period_err'])
        self.assertEqual(result['conjunction_time'], return_data['conjunction_time'])
        self.assertEqual(result['conjunction_time_err'], return_data['conjunction_time_err'])


class TestQuadraticModelEphemeris(unittest.TestCase):
    def setUp(self):
        self.ephemeris = QuadraticModelEphemeris()

    def test_quad_fit_instantiation(self):
        # Tests that ephemeris is an instance of QuadraticModelEphemeris
        self.assertIsInstance(self.ephemeris, QuadraticModelEphemeris)

    def test_quad_fit(self):
        """Tests that the quad_fit function works.

            Creates a numpy.ndarray[int] with the length of the test data
            NOTE: last one should be 626
        """
        expected_result = np.array([0. ,3.21424073e+02, 325.244054, 6.25931091e+02])
        result = self.ephemeris.quad_fit(test_epochs, 0, test_P_fits, 0, test_tra_or_occ_enum)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))

    def test_quad_fit_model(self):
        """Testing that the dictionary parameters of fit model are equal to what they are suppose to be

            Tests the creation of a dictionary named return_data containing the quadratic fit model data in the order of:
            {  
            'conjunction_time': float,
            'conjunction_time_err': float,
            'period': float,
            'period_err': float,
            'period_change_by_epoch': float,
            'period_change_by_epoch_err': float,
            }

        """
        result = self.ephemeris.fit_model(test_epochs, test_mtts, test_mtts_err, test_tra_or_occ)
        return_data = {
            'period': 1.0892663209112947,
            'period_err': 0.002368690041166098,
            'conjunction_time': 2454515.5241231285,
            'conjunction_time_err': 0.3467430587812461,
            'period_change_by_epoch': 4.223712653342504e-06,
            'period_change_by_epoch_err': 7.742732700893123e-06
        }
        self.assertEqual(result['period'], return_data['period'])
        self.assertEqual(result['period_err'], return_data['period_err'])
        self.assertEqual(result['conjunction_time'], return_data['conjunction_time'])
        self.assertEqual(result['conjunction_time_err'], return_data['conjunction_time_err'])
        self.assertEqual(result['period_change_by_epoch'], return_data['period_change_by_epoch'])
        self.assertEqual(result['period_change_by_epoch_err'], return_data['period_change_by_epoch_err'])

class TestPrecessionModelEphemeris(unittest.TestCase):
    def assertDictAlmostEqual(self, d1, d2, msg=None, places=7):
        # Helper function used to check if the dictionaries are equal to eachother
        # check if both inputs are dicts
        self.assertIsInstance(d1, dict, 'First argument is not a dictionary')
        self.assertIsInstance(d2, dict, 'Second argument is not a dictionary')
        # check if both inputs have the same keys
        self.assertEqual(d1.keys(), d2.keys())
        # check each key
        for key, value in d1.items():
            if isinstance(value, dict):
                self.assertDictAlmostEqual(d1[key], d2[key], msg=msg)
            elif isinstance(value, np.ndarray):
                self.assertTrue(np.allclose(d1[key], d2[key], rtol=1e-05, atol=1e-08))
            else:
                self.assertAlmostEqual(d1[key], d2[key], places=places, msg=msg)
    
    def setUp(self):
        self.ephemeris = PrecessionModelEphemeris()

    def test_precession_fit_instantiation(self):
        # Tests that ephemeris is an instance of PrecessionModelEphemeris
        self.assertIsInstance(self.ephemeris, PrecessionModelEphemeris)

    def test_anomalistic_period(self):
        expected_result = 1.0915939528522707
        test_dwdE =  0.000984
        result = self.ephemeris._anomalistic_period(test_P_fits, test_dwdE)
        self.assertTrue(expected_result, result)

    def test_pericenter(self):
        expected_result = np.array([1.00624,  1.295536, 1.299472, 1.570072, 1.575976, 1.590736, 1.598608])
        test_dwdE =  0.000984
        test_W0 =  2.62
        result = self.ephemeris._pericenter(test_W0, test_dwdE, test_epochs_precession)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))
        
    def test_precession_fit(self):
        """Tests that the precession_fit function works.

            Creates a numpy.ndarray[int] with the length of the test data
        """
        expected_result = np.array([-1789.93429632, -1468.50926826, -1464.14358034, -1164.54834178, -1157.99979742, -1141.62843652, -1132.89704405])
        test_W0 = 2.62
        test_dwdE = 0.000984
        test_e = 0.00310
        result = self.ephemeris.precession_fit(test_epochs_precession, 0, test_P_fits, test_dwdE, test_W0, test_e, test_tra_or_occ_enum_precession)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))

    def test_precession_fit_model(self):
        """Testing that the dictionary parameters of fit model are equal to what they are suppose to be

            Tests the creation of a dictionary named return_data containing the precession fit model data in the order of:
            {  
            'conjunction_time': float,
            'conjunction_time_err': float,
            'period': float,
            'period_err': float,
            'pericenter_change_by_epoch': float,
            'pericenter_change_by_epoch_err': float,
            'eccentricity': float,
            'eccentricity_err': float,
            'pericenter': float,
            'pericenter_err': float
            }
        """
        result = self.ephemeris.fit_model(test_epochs_precession, test_mtts_precession, test_mtts_err_precession, test_tra_or_occ_precession)
        return_data = {
            'period': 1.0914233780823739,
            'period_err': 2.5837552101593316e-06,
            'conjunction_time': 2454515.5247473116,
            'conjunction_time_err': 0.0016189004920040013,
            'pericenter_change_by_epoch': -862310.36579702,
            'pericenter_change_by_epoch_err':  1933.7369753292073,
            'eccentricity': 0.5345414535549522,
            'eccentricity_err': 13588.186664524692,
            'pericenter': -55020653.47561098,
            'pericenter_err':589049.1819169023
        }
        self.assertDictAlmostEqual(result, return_data)

class TestModelEphemerisFactory(unittest.TestCase):
    def setUp(self):
        # Initialize the Model Ephemeris Factory
        self.ephemeris = ModelEphemerisFactory()
        self.assertIsInstance(self.ephemeris, ModelEphemerisFactory)

    def test_model_no_errors_lin(self):
        # Check that linear model object is created with 'linear' type
        model = self.ephemeris.create_model('linear', test_epochs, test_mtts, test_mtts_err, test_tra_or_occ)
        self.assertIsInstance(model, dict)

    def test_model_no_errors_quad(self):
        # Check that quad model object is created with 'quadratic' type
        model = self.ephemeris.create_model('quadratic', test_epochs, test_mtts, test_mtts_err, test_tra_or_occ)
        self.assertIsInstance(model, dict)
    
    def test_model_errors(self):
        # Check that ValueError is raised if not 'linear' or 'quadratic'
        test_model_type = "invalid_model"
        with self.assertRaises(ValueError, msg=f"Invalid model type: {test_model_type}"):
            self.ephemeris.create_model(test_model_type, test_epochs, test_mtts, test_mtts_err, test_tra_or_occ)


class TestEphemeris(unittest.TestCase):
    def assertDictAlmostEqual(self, d1, d2, msg=None, places=7):
        # Helper function used to check if the dictionaries are equal to eachother
        # check if both inputs are dicts
        self.assertIsInstance(d1, dict, 'First argument is not a dictionary')
        self.assertIsInstance(d2, dict, 'Second argument is not a dictionary')
        # check if both inputs have the same keys
        self.assertEqual(d1.keys(), d2.keys())
        # check each key
        for key, value in d1.items():
            if isinstance(value, dict):
                self.assertDictAlmostEqual(d1[key], d2[key], msg=msg)
            elif isinstance(value, np.ndarray):
                self.assertTrue(np.allclose(d1[key], d2[key], rtol=1e-05, atol=1e-08))
            else:
                self.assertAlmostEqual(d1[key], d2[key], places=places, msg=msg)
                
    def setUp(self):
       """Sets up the intantiation of TimingData object and Ephemeris object.

           Runs before every test in the TestEphemeris class
       """
       self.timing_data = TimingData('jd', test_epochs, test_mtts, test_mtts_err, test_tra_or_occ, time_scale='tdb')
       self.assertIsInstance(self.timing_data, TimingData)
       self.ephemeris = Ephemeris(self.timing_data)

    def test_us_transit_times_instantiation(self):
        """Unsuccessful instantiation of the timing data object within the Ephemeris class

            Need a TimingData object to run Ephemeris
        """
        with self.assertRaises(ValueError, msg="Variable 'timing_data' expected type of object 'TimingData'."):
            self.ephemeris = Ephemeris(None)

    def test_get_model_parameters_linear(self):
        """Tests the creation of the linear model parameters

            With the input of a linear model type, the linear model parameters dictionary is created
            The dictionary is the same one from fit_model in the LinearModelEphemeris
        """
        test_model_type= 'linear'
        model_parameters = self.ephemeris._get_model_parameters(test_model_type)
        expected_result = {
            'period': 1.0904734088754364,
            'period_err': 0.0006807481006299065,
            'conjunction_time': 2454515.423966982 ,
            'conjunction_time_err': 0.23692092991744518 
        }
        self.assertDictAlmostEqual(model_parameters, expected_result)   

    def test_get_model_parameters_quad(self):
        """ Tests the creation of the quadratic model parameters

            With the input of a quadratic model type, the quadratic model parameters dictionary is created
            The dictionary is the same one from fit_model in the QuadraticModelEphemeris
        """
        test_model_type = 'quadratic'
        model_parameters = self.ephemeris._get_model_parameters(test_model_type)   
        expected_result = {
            'period': 1.0892663209112947,
            'period_err': 0.002368690041166098,
            'conjunction_time': 2454515.5241231285,
            'conjunction_time_err': 0.3467430587812461,
            'period_change_by_epoch': 4.223712653342504e-06,
            'period_change_by_epoch_err': 7.742732700893123e-06
        }
        self.assertDictAlmostEqual(model_parameters, expected_result)

    def test_k_value_linear(self):
        """Tests the correct k value is returned given the linear model type

            The k value for a linear model is 2
        """
        test_model_type = 'linear'
        expected_result = 2
        result = self.ephemeris._get_k_value(test_model_type)
        self.assertEqual(result, expected_result)
    
    def test_k_value_quad(self):
        """Tests the correct k value is returned given the quadratic model type

            The k value for a quadratic model is 3
        """
        test_model_type = 'quadratic'
        expected_result = 3
        result = self.ephemeris._get_k_value(test_model_type)
        self.assertEqual(result, expected_result)

    def test_k_value_err(self):
        """Tests the correct k value is returned given the quadratic model type

            If not 'linear' or 'quadratic', will return a ValueError
        """
        test_model_type = "invalid_type"
        with self.assertRaises(ValueError, msg="Only linear and quadratic models are supported at this time."):
            self.ephemeris._get_k_value(test_model_type)
    
    def test_calc_linear_model_uncertainties(self):
        """ Tests that the correct array of linear uncertainties are produced

            Produces a numpy array with the length of the epochs
        """
        expected_result =  np.array([0.23692092,0.31036088, 0.31190525, 0.45667354 ])
        result = self.ephemeris._calc_linear_model_uncertainties(test_T0_err_linear, test_P_err_linear)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))

    def test_calc_quad_model_uncertainties(self):
        """ Tests that the correct array of quadratic uncertainties are produced

            Produces a numpy array with the length of the epochs
        """
        expected_result = np.array([0.34674306,0.84783352,0.85829843,1.89241887])
        result = self.ephemeris._calc_quadratic_model_uncertainties(test_T0_err_quad, test_P_err_quad, test_dPdE_err)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))

    def test_calc_linear_ephemeris(self):
        """ Tests that the correct linear model data is produced

            The model data is a numpy array of calcuated mid transit times
        """
        expected_result = np.array([2454515.42396698, 2454836.5683859, 2454840.38504283, 2455140.81046697])#test model data linear
        result = self.ephemeris._calc_linear_ephemeris(test_epochs, test_P_linear, test_T0_linear)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))

    def test_calc_quadratic_ephemeris(self):
        """ Tests that the correct quadratic model data is produced

            The model data is a numpy array of calcuated mid transit times
        """
        expected_result = np.array([2454515.52412313, 2454836.49559505, 2454840.31302805, 2455140.91174185])#test model data quad
        result = self.ephemeris._calc_quadratic_ephemeris(test_epochs, test_P_quad, test_T0_quad, test_dPdE)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))

    def test_calc_chi_squared_linear(self):
        """ Tests the calculated chi squared value

            The linear chi squared value is a float that is calculated with the model data produced by test_calc_linear_ephemeris 
        """
        test_linear_model_data = np.array([2454515.42396698, 2454836.5683859, 2454840.38504283, 2455140.81046697])
        expected_result = 843766.30314325
        result = self.ephemeris._calc_chi_squared(test_linear_model_data)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))   

    def test_calc_chi_squared_quad(self):
        """ Tests the calculated chi squared value

            The quadratic chi squared value is a float that is calculated with the model data produced by test_calc_quadratic_ephemeris 
        """
        test_quad_model_data = np.array([2454515.52412313, 2454836.49559505, 2454840.31302805, 2455140.91174185])
        expected_result = 650251.5809274575
        result = self.ephemeris._calc_chi_squared(test_quad_model_data)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))   
    
    def test_get_model_ephemeris_linear(self):
        """ Tests that the linear model type produces the linear model parameters with the linear model type and linear model data included

            Uses the test_get_model_parameters_linear and test_calc_linear_ephemeris to produce a dictionary with:
            {
            'period': float,  
            'period_err': float,
            'conjunction_time': float,
            'conjunction_time_err':  float,
            'model_type': 'linear', 
            'model_data': np.array
        }
        """
        test_model_type = 'linear'
        model_parameters_linear = {
            'period': 1.0904734088754364,
            'period_err': 0.0006807481006299065,
            'conjunction_time': 2454515.423966982,
            'conjunction_time_err': 0.23692092991744518,
            'model_type': 'linear',
            'model_data': np.array([2454515.42396698, 2454836.5683859 , 2454840.38504283,
                    2455140.81046697])
        }
        result = self.ephemeris.get_model_ephemeris(test_model_type)
        self.assertDictAlmostEqual(result, model_parameters_linear)

    def test_get_model_ephemeris_quad(self):
        """ Tests that the quadratic model type produces the quadratic model parameters with the quadratic model type and quadratic model data included

            Uses the test_get_model_parameters_linear and test_calc_linear_ephemeris to produce a dictionary with:
            {
            'period': float,  
            'period_err': float,
            'conjunction_time': float,
            'conjunction_time_err':  float,
            'period_change_by_epoch': float,
            'period_change_by_epoch_err': float,
            'model_type': 'quadratic', 
            'model_data': np.array
        }
        """
        test_model_type = 'quadratic'
        model_parameters_quad = {
            'period': 1.0892663209112947,
            'period_err': 0.002368690041166098,
            'conjunction_time': 2454515.5241231285,
            'conjunction_time_err': 0.3467430587812461,
            'period_change_by_epoch': 4.223712653342504e-06,
            'period_change_by_epoch_err': 7.742732700893123e-06,
            'model_type': 'quadratic',
            'model_data': np.array([2454515.52412313, 2454836.49559505, 2454840.31302805,
                    2455140.91174185])
        }
        result = self.ephemeris.get_model_ephemeris(test_model_type)
        self.assertDictAlmostEqual(result, model_parameters_quad)

    def test_get_ephemeris_uncertainites_model_type_err(self):
        """ Unsuccessful test to calculate uncertainties

            Model type is needed
        """
        model_parameters_linear = {
            'period': 1.0904734088754364,
            'period_err': 0.0006807481006299065,
            'conjunction_time': 2454515.423966982,
            'conjunction_time_err': 0.23692092991744518,
            'model_data': np.array([2454515.42396698, 2454836.5683859 , 2454840.38504283,
                    2455140.81046697])
        }
        with self.assertRaises(KeyError, msg="Cannot find model type in model data. Please run the get_model_ephemeris method to return ephemeris fit parameters."):
            self.ephemeris.get_ephemeris_uncertainties(model_parameters_linear)
    
    def test_get_ephemeris_uncertainties_lin_err(self):
        """ Unsuccessful test to calculate uncertainties

            Period error and conjunction time error values are needed
        """
        model_parameters_linear = {
            'period': 1.0904734088754364,
            'conjunction_time': 2454515.423966982,
            'model_type': 'linear',
            'model_data': np.array([2454515.42396698, 2454836.5683859 , 2454840.38504283,
                    2455140.81046697])
        }
        with self.assertRaises(KeyError, msg="Cannot find conjunction time and period errors in model data. Please run the get_model_ephemeris method with 'linear' model_type to return ephemeris fit parameters."):
            self.ephemeris.get_ephemeris_uncertainties(model_parameters_linear)

    def test_get_ephemeris_uncertainties_quad_err(self):
        """ Unsuccessful test to calculate uncertainties

            Conjunction time error, period error and period change by epoch error is needed
        """
        model_parameters_quad = {
        'period': 1.0892663209112947,
        'conjunction_time': 2454515.5241231285,
        'period_change_by_epoch': 4.223712653342504e-06,
        'model_type': 'quadratic',
        'model_data': np.array([2454515.52412313, 2454836.49559505, 2454840.31302805,2455140.91174185])
        }
        with self.assertRaises(KeyError, msg="Cannot find conjunction time, period, and/or period change by epoch errors in model data. Please run the get_model_ephemeris method with 'quadratic' model_type to return ephemeris fit parameters."):
            self.ephemeris.get_ephemeris_uncertainties(model_parameters_quad)
   
    def test_get_ephemeris_uncertainites_linear(self):
        """ Sucessful test to calculate linear uncertainties

            Expected result is the numpy array produced by test_calc_linear_model_uncertainties
        """
        model_parameters_linear = {
            'period': 1.0904734088754364,
            'period_err': 0.0006807481006299065,
            'conjunction_time': 2454515.423966982,
            'conjunction_time_err': 0.23692092991744518,
            'model_type': 'linear',
            'model_data': np.array([2454515.42396698, 2454836.5683859 , 2454840.38504283,
                    2455140.81046697])
        }
        expected_result = np.array([0.23692092, 0.31036088, 0.31190525, 0.45667354])
        self.ephemeris.get_ephemeris_uncertainties(model_parameters_linear)
        results = self.ephemeris.get_ephemeris_uncertainties(model_parameters_linear)
        self.assertTrue(np.allclose(expected_result, results, rtol=1e-05, atol=1e-08)) 
         
    def test_get_ephemeris_uncertainites_quad(self):
        """ Sucessful test to calculate quadratic uncertainties

            Expected result is the numpy array produced by test_calc_quadratic_model_uncertaintie
        """
        model_parameters_quad = {
        'period': 1.0892663209112947,
        'period_err': 0.002368690041166098,
        'conjunction_time': 2454515.5241231285,
        'conjunction_time_err': 0.3467430587812461,
        'period_change_by_epoch': 4.223712653342504e-06,
        'period_change_by_epoch_err': 7.742732700893123e-06,
        'model_type': 'quadratic',
        'model_data': np.array([2454515.52412313, 2454836.49559505, 2454840.31302805,2455140.91174185])
        }
        expected_result = np.array([0.34674306,0.84783352,0.85829843,1.89241887])
        self.ephemeris.get_ephemeris_uncertainties(model_parameters_quad)
        results = self.ephemeris.get_ephemeris_uncertainties(model_parameters_quad)
        self.assertTrue(np.allclose(expected_result, results, rtol=1e-05, atol=1e-08)) 
         
    def test_calc_bic_lin(self):
        """ Tests the calculation of the linear bic

            Uses the linear k value and linear chi squared value
        """
        model_parameters_linear = {
            'period': 1.0904734088754364,
            'period_err': 0.0006807481006299065,
            'conjunction_time': 2454515.423966982,
            'conjunction_time_err': 0.23692092991744518,
            'model_type': 'linear',
            'model_data': np.array([2454515.42396698, 2454836.5683859 , 2454840.38504283,
                    2455140.81046697])
        }
        # k_value = 2
        expected_result = 843769.0757319723
        result = self.ephemeris.calc_bic(model_parameters_linear)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))   
        
    def test_calc_bic_quad(self):
        """ Tests the calculation of the quadratic bic

            Uses the quadratic k value and quadratic chi squared value
        """
        model_parameters_quad = {
        'period': 1.0892663209112947,
        'period_err': 0.002368690041166098,
        'conjunction_time': 2454515.5241231285,
        'conjunction_time_err': 0.3467430587812461,
        'period_change_by_epoch': 4.223712653342504e-06,
        'period_change_by_epoch_err': 7.742732700893123e-06,
        'model_type': 'quadratic',
        'model_data': np.array([2454515.52412313, 2454836.49559505, 2454840.31302805,2455140.91174185])
        }
        # k_value = 3
        expected_result = 650255.7398105409
        result = self.ephemeris.calc_bic(model_parameters_quad)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08)) 
    
    def test_calc_delta_bic(self):
        """ Tests the calulation of the delta bic

            Uses both the quadratic bic and linear bic
        """
        expected_result = 193513.33592143143
        result = self.ephemeris.calc_delta_bic() 
        self.assertTrue(expected_result, result)

    def test_subract_plotting_parameters(self):
        expected_result = np.array([-1.86264515e-09, 4.24597602e-09, 3.08841663e-09 , -2.14754436e-09])
        model_data =  np.array([2454515.42396698, 2454836.5683859 , 2454840.38504283, 2455140.81046697])
        result = self.ephemeris._subtract_plotting_parameters(model_data,test_T0_linear,test_P_linear,test_epochs)
        self.assertTrue(np.allclose(expected_result, result, rtol=1e-05, atol=1e-08))


    if __name__ == '__main__':
            unittest.main()