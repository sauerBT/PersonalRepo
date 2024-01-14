import unittest
import cstr_models_helper as ch
import numerical_methods as nm
import numpy as np

class TestCstrFunctions(unittest.TestCase):
    DECIMAL_PLACES = 4
    def test_single_cstr(self) -> None:
        MIN = 1.0
        MN  = 1.0
        YIN_X1_N1_01 = [[1.0]]
        YIN_X1_01 = [1.0]
        # m_in*(y0[x] - y[x])/Mn
        # y: listof float,y_0x: float,m_inX: float,Mn: float
        self.assertAlmostEqual(ch.single_cstr(YIN_X1_N1_01[0][0],YIN_X1_01[0],MIN,MN),0,self.DECIMAL_PLACES,"base case test")
        with self.assertRaises(Exception):
            ch.single_cstr(YIN_X1_N1_01[0][0],YIN_X1_01[0],MIN,0) #divide by zero  
        self.assertAlmostEqual(ch.single_cstr(YIN_X1_N1_01[0][0],.1,MIN,MN),-0.9,self.DECIMAL_PLACES,"normal test")

    def test_multi_1_cstr(self)-> None:
        Q1 = .5
        N3 = 3
        MIN = 1
        MN  = 1
        YI_X3_N3_01 = [[.2,.2,.2],[.5,.5,.5],[.3,.3,.3]]
        YI_X3_N3_02 = [[.2,.3,.25],[.5,.5,.5],[.3,.3,.3]]
        YIN_X3_01 = [.2,.5,.3]
        MI_N3_01 = ch.generate_mass_out_list(MIN,.5,Q1,N3) #[1,0,-.5]
        # (m_in*(y0[x] - y[x][n]) + q*m[n]*(y[x][n+1] - y[x][n]))/Mn
        # y: list[float],y_0x: float,m_inX: float,m_outX: list[float],Mn: float,backmix: float
        self.assertAlmostEqual(ch.multi_1_cstr(YI_X3_N3_01[0][0],YI_X3_N3_01[0][1],YIN_X3_01[0],0,MI_N3_01[0],MN,0),0,self.DECIMAL_PLACES,"base case test")
        with self.assertRaises(Exception):
            ch.multi_1_cstr(YI_X3_N3_01[0][0],YI_X3_N3_01[0][1],YIN_X3_01[0],MIN,MI_N3_01[0],0,Q1) #divide by zero
        self.assertAlmostEqual(ch.multi_1_cstr(YI_X3_N3_01[0][0],YI_X3_N3_01[0][1],.1,MIN,MI_N3_01[0],MN,Q1),-0.1,self.DECIMAL_PLACES,"normal test01")
        self.assertAlmostEqual(ch.multi_1_cstr(YI_X3_N3_02[0][0],YI_X3_N3_02[0][1],.1,MIN,MI_N3_01[0],MN,Q1),-0.05,self.DECIMAL_PLACES,"normal test02")

    def test_multi_x_cstr(self) -> None:
        Q1 = .5
        N3 = 3
        MIN = 1
        MN  = 1
        YI_X3_N3_01 = [[.2,.2,.2],[.5,.5,.5],[.3,.3,.3]]
        YI_X3_N3_02 = [[.2,.3,.25],[.5,.6,.55],[.3,.3,.3]]
        MI_N3_01 = ch.generate_mass_out_list(MIN,.5,Q1,N3) #[1,0,-.5]
        MI_N3_02 = [1,2,3]
        # (m[n-1]*(y[x][n-1] - y[x][n]) + q*m[n]*(y[x][n+1] - y[x][n]))/Mn
        # y_n: list[float],y_n+1: float,y_n-1: float,m_out_n: float,m_out_n-1: float,Mn: float,backmix: float
        self.assertAlmostEqual(ch.multi_x_cstr(YI_X3_N3_01[1][1],YI_X3_N3_01[1][2],YI_X3_N3_01[1][0],MI_N3_01[1],MI_N3_01[0],MN,0),0,self.DECIMAL_PLACES,"base case test")
        with self.assertRaises(Exception):
            ch.multi_x_cstr(YI_X3_N3_01[1][1],YI_X3_N3_01[1][2],YI_X3_N3_01[1][0],MI_N3_01[1],MI_N3_01[0],0,Q1) #divide by zero
        self.assertAlmostEqual(ch.multi_x_cstr(YI_X3_N3_01[1][1],YI_X3_N3_01[1][2],YI_X3_N3_01[1][0],MI_N3_01[1],MI_N3_01[0],MN,Q1),0,self.DECIMAL_PLACES,"normal test")
        self.assertAlmostEqual(ch.multi_x_cstr(YI_X3_N3_02[1][1],YI_X3_N3_02[1][2],YI_X3_N3_02[1][0],MI_N3_02[1],MI_N3_02[0],MN,Q1),-0.15,self.DECIMAL_PLACES,"normal test")

    def test_multi_N_cstr(self) -> None:
        Q1 = .5
        N3 = 3
        MIN = 1
        MN  = 1
        YI_X3_N3_01 = [[.2,.2,.2],[.5,.5,.5],[.3,.3,.3]]
        YI_X3_N3_02 = [[.2,.3,.25],[.5,.6,.55],[.3,.4,.35]]
        MI_N3_01 = ch.generate_mass_out_list(MIN,.5,Q1,N3) #[1,0,-.5]
        MI_N3_02 = [1,2,3]
        # (m[n-1]*(y[x][n-1] - y[x][n]))/Mn
        # y_n: float,y_n_1prev: float,m_out_n_prev: float,mass_n: float
        self.assertAlmostEqual(ch.multi_N_cstr(YI_X3_N3_01[2][2],YI_X3_N3_01[2][1],MI_N3_01[1],MN),0,self.DECIMAL_PLACES,"base case test")
        with self.assertRaises(Exception):
            ch.multi_x_cstr(YI_X3_N3_01[2][2],YI_X3_N3_01[2][1],MI_N3_01[1],0) #divide by zero
        self.assertAlmostEqual(ch.multi_N_cstr(YI_X3_N3_02[2][2],YI_X3_N3_02[2][1],MI_N3_02[1],MN),0.1,self.DECIMAL_PLACES,"normal test")

    def test_calculate_stream_concentration(self) -> None:
        Q1 = .5
        N1 = 1
        N3 = 3
        MIN = 1
        MN  = 1
        YI_X3_N3_01 = [[.2,.2,.2],[.5,.5,.5],[.3,.3,.3]]
        YIN_X1_N1_01 = [[1]]
        YIN_X1_01 = [1]
        YIN_X3_01 = [.2,.5,.3]
        MI_N3_01 = ch.generate_mass_out_list(MIN,.5,Q1,N3)
        MI_N1_01 = ch.generate_mass_out_list(MIN,.5,Q1,N1)
        A1_X1_n1 = ch.multi_1_cstr(YI_X3_N3_01[0][0],YI_X3_N3_01[0][1],YIN_X3_01[0],MIN,MI_N3_01[0],MN,Q1)
        A1_X1_n2 = ch.multi_x_cstr(YI_X3_N3_01[0][1],YI_X3_N3_01[0][2],YI_X3_N3_01[0][0],MI_N3_01[1],MI_N3_01[0],MN,Q1)
        A1_X1_n3 = ch.multi_N_cstr(YI_X3_N3_01[0][2],YI_X3_N3_01[0][1],MI_N3_01[1],MN)
        A1 = [A1_X1_n1,A1_X1_n2,A1_X1_n3]
        A2_X2_n1 = ch.multi_1_cstr(YI_X3_N3_01[1][0],YI_X3_N3_01[1][1],YIN_X3_01[1],MIN,MI_N3_01[0],MN,Q1)
        A2_X2_n2 = ch.multi_x_cstr(YI_X3_N3_01[1][1],YI_X3_N3_01[1][2],YI_X3_N3_01[1][0],MI_N3_01[1],MI_N3_01[0],MN,Q1)
        A2_X2_n3 = ch.multi_N_cstr(YI_X3_N3_01[1][2],YI_X3_N3_01[1][1],MI_N3_01[1],MN)
        A2 = [A2_X2_n1,A2_X2_n2,A2_X2_n3]
        A3_X3_n1 = ch.multi_1_cstr(YI_X3_N3_01[2][0],YI_X3_N3_01[2][1],YIN_X3_01[2],MIN,MI_N3_01[0],MN,Q1)
        A3_X3_n2 = ch.multi_x_cstr(YI_X3_N3_01[2][1],YI_X3_N3_01[2][2],YI_X3_N3_01[2][0],MI_N3_01[1],MI_N3_01[0],MN,Q1)
        A3_X3_n3 = ch.multi_N_cstr(YI_X3_N3_01[2][2],YI_X3_N3_01[2][1],MI_N3_01[1],MN)
        A3 = [A3_X3_n1,A3_X3_n2,A3_X3_n3]
        #y_X: list[float],y_0x: float,m_outX: list[float],Mn: float,backmix: float,m_inX: float
        self.assertEqual(ch.calculate_stream_concentration([],1,[],MN,Q1,MIN),[],"base case test")
        self.assertEqual(ch.calculate_stream_concentration(YIN_X1_N1_01[0],YIN_X1_01[0],MI_N1_01,MN,Q1,MIN),ch.single_cstr(YIN_X1_N1_01[0][0],YIN_X1_01[0],MIN,MN),"single cstr case test (N=1)")
        self.assertEqual(ch.calculate_stream_concentration(YI_X3_N3_01[0],YIN_X3_01[0],MI_N3_01,MN,Q1,MIN),A1,"multi cstr n=0 case test (N=3)")
        self.assertEqual(ch.calculate_stream_concentration(YI_X3_N3_01[1],YIN_X3_01[1],MI_N3_01,MN,Q1,MIN),A2,"multi cstr n=1 case test (N=3)")
        self.assertEqual(ch.calculate_stream_concentration(YI_X3_N3_01[2],YIN_X3_01[2],MI_N3_01,MN,Q1,MIN),A3,"multi cstr n=2 case test (N=3)")

    # def test_calculate_n_cstr(self) -> None:
    #     Q1 = .5
    #     N0 = 0
    #     N1 = 1
    #     N3 = 3
    #     MIN = 1
    #     MN  = 1
    #     YI_X3_N3_01 = [[.2,.2,.2],[.5,.5,.5],[.3,.3,.3]]
    #     YI_X1_N3_01 = [[1,1,1]]
    #     YI_X3_N1_01 = [[.2],[.5],[.3]]
    #     YIN_X1_N1_01 = [[1]]
    #     YIN_X1_01 = [1]
    #     YIN_X3_01 = [.2,.5,.3]
    #     MI_N3_01 = ch.generate_mass_out_list(MIN,.5,Q1,N3)
    #     MI_N1_01 = ch.generate_mass_out_list(MIN,.5,Q1,N1)
    #     #ch.calculate_cstr_one(),ch.calculate_cstr_x(),ch.calculate_cstr_N()],[ch.calculate_cstr_one(),ch.calculate_cstr_x(),ch.calculate_cstr_N()],[ch.calculate_cstr_one(),ch.calculate_cstr_x(),ch.calculate_cstr_N()

    #     self.assertEqual(ch.calculate_n_cstr([],[],[],MN,Q1,MIN),[],"base case test (X=0,N=0)")
    #     self.assertEqual(ch.calculate_n_cstr([],[],[],MN,Q1,MIN),[],"base case test (X=0,N=0)")
    #     self.assertEqual(ch.calculate_n_cstr([],[],[],MN,Q1,MIN),[],"base case test (X=0,N=0)")
    #     self.assertEqual(ch.calculate_n_cstr([],[],MI_N1_01,MN,Q1,MIN),[],"base case test(X=0,N=1)")
    #     self.assertEqual(ch.calculate_n_cstr([],[1],[],MN,Q1,MIN),[],"base case test (X=1,N=0)")
    #     self.assertEqual(ch.calculate_n_cstr(YIN_X1_N1_01,YIN_X1_01,MI_N1_01,MN,Q1,MIN),[ch.calculate_stream_concentration(YIN_X1_N1_01[0],YIN_X1_01[0],MI_N1_01,MN,Q1,MIN)],"test (X=1,N=1)")
    #     self.assertEqual(ch.calculate_n_cstr(YI_X1_N3_01,YIN_X1_01,MI_N3_01,MN,Q1,MIN),[ch.calculate_stream_concentration(YI_X1_N3_01[0],YIN_X1_01[0],MI_N3_01,MN,Q1,MIN)],"test (X=1,N=3)")
    #     self.assertEqual(ch.calculate_n_cstr(YI_X3_N1_01,YIN_X3_01,MI_N1_01,MN,Q1,MIN),[ch.calculate_stream_concentration(YI_X3_N1_01[0],YIN_X3_01[0],MI_N1_01,MN,Q1,MIN),
    #                                                                               ch.calculate_stream_concentration(YI_X3_N1_01[1],YIN_X3_01[1],MI_N1_01,MN,Q1,MIN),
    #                                                                               ch.calculate_stream_concentration(YI_X3_N1_01[2],YIN_X3_01[2],MI_N1_01,MN,Q1,MIN)],"test (X=3,N=1)") 
    #     self.assertEqual(ch.calculate_n_cstr(YI_X3_N3_01,YIN_X3_01,MI_N3_01,MN,Q1,MIN),[ch.calculate_stream_concentration(YI_X3_N3_01[0],YIN_X3_01[0],MI_N3_01,MN,Q1,MIN),
    #                                                                               ch.calculate_stream_concentration(YI_X3_N3_01[1],YIN_X3_01[1],MI_N3_01,MN,Q1,MIN),
    #                                                                               ch.calculate_stream_concentration(YI_X3_N3_01[2],YIN_X3_01[2],MI_N3_01,MN,Q1,MIN)],"Test (N=3,X=3)") 

    def test_replay_ode_funcs(self) -> None:

        Q1 = .5
        YI_X3_N3_01 = [[.2,.2,.2],[.5,.5,.5],[.3,.3,.3]]
        YI_X1_N3_01 = [[1,1,1]]
        YI_X3_N1_01 = [[.2],[.5],[.3]]
        YIN_X1_N1_01 = [[1]]
        YIN_X1_01 = [[1]]
        mass = [1000,1010,1030]
        mass_in = [1,1,1]
        dmdt0 = ch.change_in_mass([1000])
        dmdt1 = ch.change_in_mass(mass)
        YIN_X3_01 = [[.2,.5,.3],[.2,.5,.3],[.2,.5,.3]]
        MI_N1_01 = ch.generate_mass_out_list(mass_in[0],.5,0,1)
        MI_N3_01 = [ch.generate_mass_out_list(mass_in[0],.5,0,3),
                    ch.generate_mass_out_list(mass_in[1],.5,0,3),
                    ch.generate_mass_out_list(mass_in[2],.5,0,3)]
        [x_n,A1] = nm.rk4_2d(ch.calculate_n_cstr,x0 = 0,y0 = YI_X3_N3_01,xn = 1,n=10,args=(YIN_X3_01[0],mass[0],dmdt1[0],0,mass_in[0]))
        [x_n,A2] = nm.rk4_2d(ch.calculate_n_cstr,x0 = 0,y0 = A1[9,::],xn = 1,n=10,args=(YIN_X3_01[1],mass[1],dmdt1[1],0,mass_in[1]))
        [x_n,A3] = nm.rk4_2d(ch.calculate_n_cstr,x0 = 0,y0 = A2[9,::],xn = 1,n=10,args=(YIN_X3_01[2],mass[2],dmdt1[2],0,mass_in[2]))
        # (y: list[list[float]], t, y0: list[float], mass: float, dMdt: float, backmix: float, m_in: float):
        #np.testing.assert_allclose(ch.replay_ode_funcs(ch.calculate_n_cstr,[],[([],0,dmdt0[0],0,0)]),np.array([]))
        #self.assertEqual(ch.replay_ode_funcs(ch.n_cstr_ode,YIN_X1_N1_01,[(YIN_X1_01[0],mass[0],0,mass_in[0])]),[ch.n_cstr_ode(YIN_X1_N1_01,YIN_X1_01[0],MI_N1_01,mass[0],0,mass_in[0])],"single cstr single input test 1")
        np.testing.assert_allclose(ch.replay_ode_funcs(ch.calculate_n_cstr,YI_X3_N3_01,[(YIN_X3_01[0],mass[0],dmdt1[0],0,mass_in[0]),
                                                                        (YIN_X3_01[1],mass[1],dmdt1[1],0,mass_in[1]),
                                                                        (YIN_X3_01[2],mass[2],dmdt1[2],0,mass_in[2])]),[A1,
                                                                                                                        A2,
                                                                                                                        A3])

    def test_generate_initial_conditions(self) -> None:
        self.assertEqual(ch.generate_initial_conditions([],1),[],"base case test")
        self.assertEqual(ch.generate_initial_conditions([1],1),[[1]],"1 element array given 1 case test")
        self.assertEqual(ch.generate_initial_conditions([1],3),[[1,1,1]],"1 element array given 3 case test")
        self.assertEqual(ch.generate_initial_conditions([.2,.5,.3],1),[[.2],[.5],[.3]],"3 element array given 1 case test")
        self.assertEqual(ch.generate_initial_conditions([.2,.5,.3],3),[[.2,.2,.2],[.5,.5,.5],[.3,.3,.3]],"3 element array given 3 case test")

    def test_calculate_n_cstr (self) -> None:
        #(y: list[list[float]], t, y0: list[float], mass: float, dMdt: float, backmix: float, m_in: float):
        Q1 = .5
        N0 = 0
        N1 = 1
        N3 = 3
        MIN = 1
        MN  = 1010
        dmdt0 = 0
        dmdt1 = 10
        YI_X3_N3_01 = [[.2,.2,.2],[.5,.5,.5],[.3,.3,.3]]
        YI_X1_N3_01 = [[1,1,1]]
        YI_X3_N1_01 = [[.2],[.5],[.3]]
        YIN_X1_N1_01 = [[1]]
        YIN_X1_01 = [1]
        YIN_X3_01 = [.2,.5,.3]
        MI_N3_01 = ch.generate_mass_out_list(MIN,dmdt1,Q1,N3)
        MI_N1_01 = ch.generate_mass_out_list(MIN,dmdt1,Q1,N1)

        np.testing.assert_allclose(ch.calculate_n_cstr([],0,[],0,0,0,0,1),[])#,"base case test 1")
        np.testing.assert_allclose(ch.calculate_n_cstr([],0,[1],MN,dmdt1,Q1,MIN,1),np.array([ch.calculate_stream_concentration([1],1,MI_N1_01,MN,Q1,MIN)]))#,"X=1,N=1 Test inferred input")
        np.testing.assert_allclose(ch.calculate_n_cstr([],0,[1],MN,dmdt1,Q1,MIN,3),np.array([ch.calculate_stream_concentration([1,1,1],1,MI_N3_01,MN,Q1,MIN)]))#,"X=1,N=3 Test inferred input")
        np.testing.assert_allclose(ch.calculate_n_cstr([],0,[.2,.5,.3],MN,dmdt1,Q1,MIN,1),np.array([ch.calculate_stream_concentration([.2],.2,MI_N1_01,MN,Q1,MIN),
                                                                                    ch.calculate_stream_concentration([.5],.5,MI_N1_01,MN,Q1,MIN),
                                                                                    ch.calculate_stream_concentration([.3],.3,MI_N1_01,MN,Q1,MIN)]))#,"X=3,N=1 Test inferred input")
        np.testing.assert_allclose(ch.calculate_n_cstr([],0,[.2,.5,.3],MN,dmdt1,Q1,MIN,3),np.array([ch.calculate_stream_concentration([.2,.2,.2],.2,MI_N3_01,MN,Q1,MIN),
                                                                                    ch.calculate_stream_concentration([.5,.5,.5],.5,MI_N3_01,MN,Q1,MIN),
                                                                                    ch.calculate_stream_concentration([.3,.3,.3],.3,MI_N3_01,MN,Q1,MIN)]))#,"X=3,N=3 Test inferred input")
        np.testing.assert_allclose(ch.calculate_n_cstr(YIN_X1_N1_01,0,YIN_X1_01,MN,dmdt1,Q1,MIN),np.array([ch.calculate_stream_concentration(YIN_X1_N1_01[0],YIN_X1_01[0],MI_N1_01,MN,Q1,MIN)]))#,"test (X=1,N=1)")
        np.testing.assert_allclose(ch.calculate_n_cstr(YI_X1_N3_01,0,YIN_X1_01,MN,dmdt1,Q1,MIN),[ch.calculate_stream_concentration(YI_X1_N3_01[0],YIN_X1_01[0],MI_N3_01,MN,Q1,MIN)]) #"test (X=1,N=3)"
        np.testing.assert_allclose(ch.calculate_n_cstr(YI_X3_N1_01,0,YIN_X3_01,MN,dmdt1,Q1,MIN),[ch.calculate_stream_concentration(YI_X3_N1_01[0],YIN_X3_01[0],MI_N1_01,MN,Q1,MIN),
                                                                                                ch.calculate_stream_concentration(YI_X3_N1_01[1],YIN_X3_01[1],MI_N1_01,MN,Q1,MIN),
                                                                                                ch.calculate_stream_concentration(YI_X3_N1_01[2],YIN_X3_01[2],MI_N1_01,MN,Q1,MIN)]) #,"test (X=3,N=1)") 
        np.testing.assert_allclose(ch.calculate_n_cstr(YI_X3_N3_01,0,YIN_X3_01,MN,dmdt1,Q1,MIN),[ch.calculate_stream_concentration(YI_X3_N3_01[0],YIN_X3_01[0],MI_N3_01,MN,Q1,MIN),
                                                                                            ch.calculate_stream_concentration(YI_X3_N3_01[1],YIN_X3_01[1],MI_N3_01,MN,Q1,MIN),
                                                                                            ch.calculate_stream_concentration(YI_X3_N3_01[2],YIN_X3_01[2],MI_N3_01,MN,Q1,MIN)])#,"Test (N=3,X=3)") 

    def test_change_in_mass(self)-> None:
        M0 = []
        M1 = [1000]
        M2 = [1000,1010,1030]
        self.assertEqual(ch.change_in_mass(M0),[],"base case test")
        self.assertEqual(ch.change_in_mass(M1),[0],"single input test")
        self.assertEqual(ch.change_in_mass(M2),[0,10,20],"three input test")

    def test_generate_mass_out_list(self) -> None:
        # m_in: float,dMndt: float,backmix: float,number_of_cstr: int
        self.assertEqual(ch.generate_mass_out_list(1,1,.5,0), [],"N=0 test") # base case test
        self.assertEqual(ch.generate_mass_out_list(1,1,.5,1), [0], "N=1, mass in == change in mass test")
        self.assertEqual(ch.generate_mass_out_list(1,0,.5,1), [1], "N=1, mass in != change in mass test")
        self.assertEqual(ch.generate_mass_out_list(1,.5,.5,3), [1,0,-.5],"N=3 test")
        with self.assertRaises(Exception):
            ch.generate_mass_out_list(1,1,1,3)
        with self.assertRaises(Exception):
            ch.generate_mass_out_list(1,1,-.01,3)
        self.assertEqual(ch.generate_mass_out_list(1,0,1,1), [1], "N=1, mass in != change in mass, backmix out of range test")

if __name__ == '__main__':
    unittest.main()