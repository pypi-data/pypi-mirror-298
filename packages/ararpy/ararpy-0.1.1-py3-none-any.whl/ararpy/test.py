#  Copyright (C) 2024 Yang. - All Rights Reserved
"""
# ==========================================
# Copyright 2024 Yang
# ararpy - test.py
# ==========================================
#
#
#
"""
import ararpy as ap
import os
import ctypes
import numpy as np
import time

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class DiffSample:
    def __init__(self, smp = None, name: str = None):

        if smp is not None:
            self.smp = smp
            self.sname = self.smp.name()

            self.sequence = self.smp.sequence()
            self.ni = self.sequence.size  # sequence number

            # self.telab = np.linspace(600, 1500, self.ni, dtype=np.float64)
            self.telab = np.array(self.smp.TotalParam[124], dtype=np.float64)

            ### 这里用真实的加热温度之后 a1 > 0，导致后面无法计算
            ### 原因：telab不能为 0


            self.telab = self.telab + 275.13
            # self.tilab = np.array([15*60 for i in range(self.ni)], dtype=np.float64)
            self.tilab = np.array(self.smp.TotalParam[123], dtype=np.float64)
            self.a39 = np.array(self.smp.DegasValues[20], dtype=np.float64)
            self.sig39 = np.array(self.smp.DegasValues[21], dtype=np.float64)
            self.f = np.cumsum(self.a39) / self.a39.sum()
            self.f[-1] = 0.999999999
            # self.f = np.insert(self.f, 0, 0)
            self.ya = np.array(self.smp.ApparentAgeValues[2], dtype=np.float64)
            self.sig = np.array(self.smp.ApparentAgeValues[3], dtype=np.float64)

            loc = "D:\\PythonProjects\\ararpy_package\\ararpy\\examples"
            self.file_age_in = open(os.path.join(loc, f"{self.sname}_age.in"), "w")
            self.file_sig_in = open(os.path.join(loc, f"{self.sname}_sig.in"), "w")
            self.file_tmp_in = open(os.path.join(loc, f"{self.sname}_tmp.in"), "w")
            self.file_fj_in = open(os.path.join(loc, f"{self.sname}_fj.in"), "w")
            self.file_a39_in = open(os.path.join(loc, f"{self.sname}_a39.in"), "w")

            self.file_age_in.writelines("\n".join([f"  {self.f[i] * 100}  {self.ya[i]}" for i in range(self.ni)]))
            self.file_sig_in.writelines("\n".join([f"{self.sig[i]}" for i in range(self.ni)]))
            self.file_tmp_in.writelines(f"{str(self.ni)}\n")
            self.file_tmp_in.writelines("\n".join([f"{self.telab[i]}\n{self.tilab[i]}" for i in range(self.ni)]))
            self.file_fj_in.writelines("\n".join([f"{self.f[i]}" for i in range(self.ni)]))
            self.file_a39_in.writelines("\n".join([f"  {self.a39[i]}  {self.sig39[i]}" for i in range(self.ni)]))

            self.file_age_in.close()
            self.file_sig_in.close()
            self.file_tmp_in.close()
            self.file_fj_in.close()
            self.file_a39_in.close()


        elif name is not None:
            self.sname = name
        else:
            raise ValueError("Sample not found")

        self.pi = 3.141592654
        self.nloop = 1
        self.ngauss = 10
        self.zi = [0.]
        self.b = 8
        self.imp = 2
        self.acut = 0.5
        self.dchmin = 0.01
        self.ncons = 0
        self.ndom = 8
        self.mdom = 8
        self.iset = 0
        self.gset = 0
        self.wt = []


class DiffAgemonFuncs(DiffSample):

    def __init__(self, ni=10, mmax=100, ochisq=0, **kwargs):

        self.ni = ni
        self.mmax = mmax
        self.ochisq = ochisq

        super().__init__(**kwargs)

        self.nca = 200
        self.da = np.zeros(self.ni, dtype=np.float64)
        self.beta = np.zeros(self.mmax, dtype=np.float64)
        self.atry = np.zeros(self.mmax, dtype=np.float64)

        # constants
        self.nwcy = 10
        self.ncyc = 1
        self.ntst = 1001
        self.ns = 200
        self.nmaxi = np.zeros(self.nwcy, dtype=int)
        self.nmaxo = np.zeros(self.nwcy, dtype=int)
        self.tti = np.zeros([self.nwcy, 2, self.ntst], dtype=np.float64)
        self.tto = np.zeros([self.nwcy, 2, self.ntst], dtype=np.float64)
        self.agei = np.zeros([self.nwcy, 2, self.ns], dtype=np.float64)
        self.ageo = np.zeros([self.nwcy, 2, self.ns], dtype=np.float64)

        self.loc = "D:\\PythonProjects\\ararpy_package\\ararpy\\examples"

        self.file_ame_in = open(os.path.join(self.loc, f"{self.sname}.ame"), "r")  # from arrmulti
        self.file_age_in = open(os.path.join(self.loc, f"{self.sname}_age.in"), "r")
        self.file_sig_in = open(os.path.join(self.loc, f"{self.sname}_sig.in"), "r")
        self.file_tmp_in = open(os.path.join(self.loc, f"{self.sname}_tmp.in"), "r")

        self.file_output_mch = open(os.path.join(self.loc, f"{self.sname}_mch-out.dat"), "w")
        self.file_output_mages = open(os.path.join(self.loc, f"{self.sname}_mages-out.dat"), "w")
        self.file_output_agesd = open(os.path.join(self.loc, f"{self.sname}_ages-sd.samp"), "w")

        self.file_output_mch.close()
        self.file_output_mages.close()
        self.file_output_agesd.close()

        # parameters
        self.ns = 200
        self.nc = 100
        self.ntst = 1001
        self.mxi = 350
        self.nn = 319
        self.mfit = 10
        self.nwcy = 10
        self.nd = 10
        self.xlambd = 0.0005543
        self.a = 0
        self.perc = 0.01
        self.cht0 = 1.0e-4
        self.nrun = 5
        self.maxrun = 15
        self.nemax = 10

        # 读取加热温度和时间
        self.ni = int(self.file_tmp_in.readline())
        self.nit = self.ni
        self.r39 = np.zeros(self.ni, dtype=np.float64)
        self.telab = np.zeros(self.ni, dtype=np.float64)
        self.tilab = np.zeros(self.ni, dtype=np.float64)
        for i in range(self.ni):
            self.telab[i] = float(self.file_tmp_in.readline())
            self.tilab[i] = float(self.file_tmp_in.readline())
            if self.telab[i] > 1373:
                # go to 11
                self.ni = i
                break
            self.tilab[i] /= 5.256E+11  # 1 Ma = 525600000000 minutes

        # 读取
        nemax = 0
        self.nst_arr = np.zeros(100, dtype=int)
        self.e_arr = np.zeros(100, dtype=np.float64)
        self.d0_arr = np.zeros([100, 20], dtype=np.float64)
        self.vc_arr = np.zeros([100, 20], dtype=np.float64)
        self.e = 0
        self.d0 = np.zeros(self.nd, dtype=np.float64)
        self.vc = np.zeros(self.nd, dtype=np.float64)
        kk = 0
        while True:
            try:
                self.nst_arr[kk] = int(self.file_ame_in.readline())  # sequence number
                # self.nst = int(self.file_ame_in.readline())  # sequence number
                for i in range(self.nst_arr[kk]):
                    self.e_arr[kk] = float(self.file_ame_in.readline())
                    self.d0_arr[kk, i] = 10 ** float(self.file_ame_in.readline()) / 4 * (24 * 3600 * 365e+6)
                    self.vc_arr[kk, i] = float(self.file_ame_in.readline())
                    # self.e = float(self.file_ame_in.readline())
                    # self.d0[i] = float(self.file_ame_in.readline())
                    # self.vc[i] = float(self.file_ame_in.readline())
                    # self.d0[i] = 10 ** self.d0[i] / 4 * (24 * 3600 * 365e+6)
                    nemax += 1
                self.atmp = self.file_ame_in.readline()
                self.atmp = self.file_ame_in.readline()
                self.atmp = self.file_ame_in.readline()
                kk += 1
            except ValueError:
                break
        self.kk = kk
        print(f"{self.kk = }")

        # 读取sig
        self.sig = np.zeros(self.ns, dtype=np.float64)
        self.xs = np.zeros(self.ns + 1, dtype=np.float64)
        self.ya = np.zeros(self.ns + 1, dtype=np.float64)
        for i in range(self.nit + 1):
            try:
                self.sig[i] = float(self.file_sig_in.readline())
                if self.sig[i] <= 0:
                    raise ValueError("Sigma less than 0")
                self.xs[i + 1], self.ya[i + 1] = [float(j) for j in filter(lambda x: is_number(x),
                                                                           self.file_age_in.readline().split(' '))]
                self.xs[i + 1] /= 100
                if self.ya[i] < 0:
                    self.ya[i] = 0
            except ValueError:
                print(f"{i = } error in reading sig file")
            continue

        self.max_plateau_age = 30

        self.file_ame_in.close()
        self.file_tmp_in.close()
        self.file_age_in.close()
        self.file_sig_in.close()






def test():
    example_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'examples')
    print(f"Running: ararpy.test()")
    print(f"============= Open an example .arr file =============")
    # file_path = os.path.join(example_dir, r'22WHA0433.arr')
    # sample = ap.from_arr(file_path=file_path)
    # # file_path = os.path.join(example_dir, r'22WHA0433.age')
    # # sample = ap.from_age(file_path=file_path)
    # print(f"{file_path = }")
    # print(f"sample = from_arr(file_path=file_path)")
    # print(f"{sample.name() = }")
    # print(f"{sample.help = }")
    # print(f"sample.parameters() = {sample.parameters()}")
    # print(f"sample.parameters().to_df() = \n{sample.parameters().to_df()}")
    # print(sample.show_data())
    # print(sample.sample())
    # print(sample.blank().to_df().iloc[:, [1, 2, 3]])

    # diff_smp = ap.calc.diffusion_funcs.DiffArrmultiFunc(smp=sample)
    # diff_smp = ap.calc.diffusion_funcs.DiffArrmultiFunc(name='12h')
    # e, sige, ordi, sigo = diff_smp.main()
    # diff_smp = ap.calc.diffusion_funcs.DiffAgemonFuncs(smp=sample)
    # diff_smp = ap.calc.diffusion_funcs.DiffAgemonFuncs(name='12h')
    # diff_smp.main()
    # diff_smp = ap.calc.diffusion_funcs.DiffDraw(name='12h')
    # diff_smp.main()


    # diff_smp = ap.calc.diffusion_funcs.InsideTemperatureCalibration()
    #
    # # k1, k2 = diff_smp.get_calibrated_temp(45 * 60, 600)
    # # print(round((k1 + k2) / 2, 2), round(abs(k2 - k1) / 2, 2))
    #
    # ## 显示每个设定温度的所有空载加热测试结果，红蓝线为上下95%置信区间
    # diff_smp.plot()
    #
    # ## 显示用于校正的温度曲线
    # diff_smp.plot_confidence()

    ## 显示实际样品的 libano 记录，并给出校正的温度曲线
    # diff_smp.plot_libano_log(r"C:\Users\Young\OneDrive\Documents\Libano Data\2024-03-26\202403260941-libano.log")
    # diff_smp.plot_libano_log(r"C:\Users\Young\OneDrive\00-Projects\【2】个人项目\2022-05论文课题\【3】分析测试\ArAr\01-VU实验数据和记录\20240717-Y53\202407171832-libano.log")
    # diff_smp.plot_libano_log(r"C:\Users\Young\OneDrive\00-Projects\【2】个人项目\2022-05论文课题\【3】分析测试\ArAr\01-VU实验数据和记录\20240714-Y52\202407142127-libano.log")

    name = "20240909-Y86"
    arr_name = "20240909_24BY86"

    libano_log_path = f"C:\\Users\\Young\\OneDrive\\00-Projects\\【2】个人项目\\2022-05论文课题\\【3】分析测试\\ArAr\\01-VU实验数据和记录\\{name}\\Libano-log"
    # libano_log_path = r"C:\Users\Young\OneDrive\00-Projects\【2】个人项目\2022-05论文课题\【3】分析测试\ArAr\01-VU实验数据和记录\20240705-Y50\Libano-log"
    libano_log_path = [os.path.join(libano_log_path, i) for i in os.listdir(libano_log_path)]
    print(libano_log_path)
    helix_log_path = f"C:\\Users\\Young\\OneDrive\\00-Projects\\【2】个人项目\\2022-05论文课题\\【3】分析测试\\ArAr\\01-VU实验数据和记录\\{name}\\LogFiles"
    # helix_log_path = r"C:\Users\Young\OneDrive\00-Projects\【2】个人项目\2022-05论文课题\【3】分析测试\ArAr\01-VU实验数据和记录\20240621-Y56\LogFiles-20240621"
    helix_log_path = [os.path.join(helix_log_path, i) for i in os.listdir(helix_log_path)]
    print(helix_log_path)

    loc = f"C:\\Users\\Young\\OneDrive\\00-Projects\\【2】个人项目\\2022-05论文课题\\【3】分析测试\\ArAr\\01-VU实验数据和记录\\{name}"
    arr_path = f"C:\\Users\\Young\\OneDrive\\00-Projects\\【2】个人项目\\2022-05论文课题\\【3】分析测试\\ArAr\\01-VU实验数据和记录\\Arr Data\\{arr_name}.arr"
    diff_smp = ap.calc.diffusion_funcs.SmpTemperatureCalibration(libano_log_path=libano_log_path, helix_log_path=helix_log_path, arr_path=arr_path, loc=loc)



###  梳理这些函数  用numba加速

if __name__ == "__main__":
    test()
