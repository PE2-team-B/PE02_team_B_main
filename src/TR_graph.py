# 라이브러리 import
with open('library.txt','r') as f:
    for library in f:
        exec(library)
import functions as fc
import math
warnings.filterwarnings('ignore',category=np.RankWarning)
'''
def plot_TR_graph(Wafer,Date,Position):

    wave_len = np.array([])
    wave_len_ref = np.array([])
    trans = np.array([])
    wave_len_half = []
    trans_half = []
    trans_ref = np.array([])
    wave_len_max = []
    trans_max = []
    bias = []
    I = np.array([])
    smoothed_trans = np.array([])
    temp1 = 0
    temp2 = 0

    path = os.path.join('..','dat',Wafer,Date)
    file_name = [os.path.join(path,f) for f in os.listdir(path) if 'LMZ' in f and f.endswith('.xml') and Position in f]

    tree = elemTree.parse(file_name[0])
    root = tree.getroot()

    for modulator in root.iter('Modulator'):
        for WL_sweep in modulator.iter('WavelengthSweep'):
            if temp1 == 1:
                wave_len_ref = np.append(wave_len_ref, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
                trans_ref = np.append(trans_ref, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
                continue
            wave_len = np.append(wave_len, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
            trans = np.append(trans, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
            bias.append(float(WL_sweep.attrib['DCBias']))
            temp2 += 1
        temp1 += 1
    wave_len = wave_len.reshape(temp2,int(trans.size/temp2))
    trans = trans.reshape(temp2,int(trans.size/temp2))
    fit_trans_ref = fc.Ref_fitted_data(wave_len_ref,trans_ref)
    s = 150
    for i in range(wave_len.shape[0]):
        trans[i] = trans[i] - fit_trans_ref
        # plt.plot(wave_len[i],trans[i])
        trans_half_temp = []
        wave_len_half_temp = []
        for k in range(wave_len.shape[1]):
            count = 0
            if k >= (wave_len.shape[1]-(s+1)):
                continue
            for g in range(1,(s+1)):
                if trans[i][k] > trans[i][k+g]:
                    count += 1
            if count >= s-3:
                trans_half_temp.append(trans[i][k])
                wave_len_half_temp.append(wave_len[i][k])
        wave_len_half.append(wave_len_half_temp)
        trans_half.append(trans_half_temp)
        # plt.plot(wave_len_half[i],trans_half[i],'ro',markersize=0.5)#######
    # plt.show()

    for i in range(len(wave_len_half)):
        wave_len_max_temp = []
        trans_max_temp = []
        for j in range(len(wave_len_half[i])):
            if j == 0:
                wave_len_max_temp.append(wave_len_half[i][j])
                trans_max_temp.append(trans_half[i][j])
                continue
            elif j >= len(wave_len_half[i]) - 4:
                continue
            if (wave_len_half[i][j + 2] - wave_len_half[i][j + 1]) >= (wave_len_half[i][j + 1] - wave_len_half[i][j] + 4):
                wave_len_max_temp.append(wave_len_half[i][j + 2])
                trans_max_temp.append(trans_half[i][j + 2])

        if trans_max_temp[0] < trans_max_temp[1]+0.5:
            wave_len_max.append(wave_len_max_temp[1:])
            trans_max.append(trans_max_temp[1:])
        else:
            wave_len_max.append(wave_len_max_temp)
            trans_max.append(trans_max_temp)

        # print(wave_len_max_temp,trans_max_temp)
        # plt.plot(wave_len_max[i],trans_max[i],'ro')
        # plt.plot(wave_len[i],fc.flat_fit_function(np.array(wave_len_max[i]), np.array(trans_max[i]))(wave_len[i]))
        trans[i] = trans[i] - fc.flat_fit_function(np.array(wave_len_max[i]), np.array(trans_max[i]))(wave_len[i]) # flatten 한 데이터들로 다시 trans 변수를 할당
        # plt.plot(wave_len[i],trans[i],'b-')
        I = np.append(I,10**(trans[i]/10)/1000)
    # print(I)
    I = I.reshape(temp2,int(len(I)/temp2))
    # for i in range(temp2):
    #     plt.plot(wave_len[i],I[i])
    # 극댓값 정보를 찾기 -> 여러개 시도
    # print(I[bias.index(0.0)], wave_len[bias.index(0.0)])
    # print(bias)
    n_eff = fc.Transmission_fitting_n_eff(wave_len,I,bias)
    del_n_eff = []
    # fc.Transmission_fitting_n_eff_V(wave_len, I, n_eff, bias, 0.5)
    for bia in bias:
       if bia == 0.0:
           del_n_eff.append(0.0)
           continue
       del_n_eff.append(fc.Transmission_fitting_n_eff_V(wave_len, I, n_eff, bias, bia)[0])
    plt.show()
    plt.plot(bias,del_n_eff,'r-')
    # print(trans_max[bias.index(0.0)])
    plt.axhline(0, color='black')  # x축에 대한 수평선
    plt.axvline(0, color='black')  # y축에 대한 수직선
    plt.grid()
    plt.show()
'''
class plot_TR:
    def __init__(self,Wafer,Date,Position):
        self.Wafer = Wafer
        self.Date = Date
        self.Position = Position
        self.label_font_properties = {'family':'serif','size':12}
        self.title_font_properties = {'family':'serif','size':15,'weight':'bold'}
    def data_parse(self):
        self.wave_len = np.array([])
        self.wave_len_ref = np.array([])
        self.trans = np.array([])
        wave_len_half = []
        trans_half = []
        self.trans_ref = np.array([])
        wave_len_max = []
        trans_max = []
        self.bias = []
        self.I = np.array([])
        # smoothed_trans = np.array([])
        temp1 = 0
        temp2 = 0

        path = os.path.join('..', 'dat', self.Wafer, self.Date)
        file_name = [os.path.join(path, f) for f in os.listdir(path) if
                     'LMZ' in f and f.endswith('.xml') and self.Position in f]

        tree = elemTree.parse(file_name[0])
        root = tree.getroot()

        for modulator in root.iter('Modulator'):
            for WL_sweep in modulator.iter('WavelengthSweep'):
                if temp1 == 1:
                    self.wave_len_ref = np.append(self.wave_len_ref, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
                    self.trans_ref = np.append(self.trans_ref, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
                    continue
                self.wave_len = np.append(self.wave_len, np.array(list(map(float, WL_sweep.find('L').text.split(',')))))
                self.trans = np.append(self.trans, np.array(list(map(float, WL_sweep.find('IL').text.split(',')))))
                self.bias.append(float(WL_sweep.attrib['DCBias']))
                temp2 += 1
            temp1 += 1
        self.wave_len = self.wave_len.reshape(temp2, int(self.trans.size / temp2))
        self.trans = self.trans.reshape(temp2, int(self.trans.size / temp2))
        fit_trans_ref = fc.Ref_fitted_data(self.wave_len_ref, self.trans_ref)
        s = 150
        for i in range(self.wave_len.shape[0]):
            self.trans[i] = self.trans[i] - fit_trans_ref
            # plt.plot(wave_len[i],trans[i])
            trans_half_temp = []
            wave_len_half_temp = []
            for k in range(self.wave_len.shape[1]):
                count = 0
                if k >= (self.wave_len.shape[1] - (s + 1)):
                    continue
                for g in range(1, (s + 1)):
                    if self.trans[i][k] > self.trans[i][k + g]:
                        count += 1
                if count >= s - 3:
                    trans_half_temp.append(self.trans[i][k])
                    wave_len_half_temp.append(self.wave_len[i][k])
            wave_len_half.append(wave_len_half_temp)
            trans_half.append(trans_half_temp)
            # plt.plot(wave_len_half[i],trans_half[i],'ro',markersize=0.5)#######
        # plt.show()

        for i in range(len(wave_len_half)):
            wave_len_max_temp = []
            trans_max_temp = []
            for j in range(len(wave_len_half[i])):
                if j == 0:
                    wave_len_max_temp.append(wave_len_half[i][j])
                    trans_max_temp.append(trans_half[i][j])
                    continue
                elif j >= len(wave_len_half[i]) - 4:
                    continue
                if (wave_len_half[i][j + 2] - wave_len_half[i][j + 1]) >= (
                        wave_len_half[i][j + 1] - wave_len_half[i][j] + 4):
                    wave_len_max_temp.append(wave_len_half[i][j + 2])
                    trans_max_temp.append(trans_half[i][j + 2])

            if trans_max_temp[0] < trans_max_temp[1] + 0.5:
                wave_len_max.append(wave_len_max_temp[1:])
                trans_max.append(trans_max_temp[1:])
            else:
                wave_len_max.append(wave_len_max_temp)
                trans_max.append(trans_max_temp)

            # print(wave_len_max_temp,trans_max_temp)
            # plt.plot(wave_len_max[i],trans_max[i],'ro')
            # plt.plot(wave_len[i],fc.flat_fit_function(np.array(wave_len_max[i]), np.array(trans_max[i]))(wave_len[i]))
            self.trans[i] = self.trans[i] - fc.flat_fit_function(np.array(wave_len_max[i]), np.array(trans_max[i]))(self.wave_len[i])  # flatten 한 데이터들로 다시 trans 변수를 할당
            # plt.plot(wave_len[i],trans[i],'b-')
            self.I = np.append(self.I, 10 ** (self.trans[i] / 10) / 1000)
        # print(I)
        self.I = self.I.reshape(temp2, int(len(self.I) / temp2))
        # for i in range(temp2):
        #     plt.plot(wave_len[i],I[i])
        # 극댓값 정보를 찾기 -> 여러개 시도
        # print(I[bias.index(0.0)], wave_len[bias.index(0.0)])
        # print(bias)
    def fitted_TR_graph_plot(self):
        self.del_n_eff = []
        result_n_eff = fc.Transmission_fitting_n_eff(self.wave_len, self.I, self.bias)
        n_eff = result_n_eff[0]
        for bia in self.bias:
            if bia == 0.0:
                self.del_n_eff.append(0.0)
                plt.plot(self.wave_len[self.bias.index(0.0)],fc.Transmission_fitting_n_eff(self.wave_len, self.I, self.bias)[1],linewidth=0.8,label=f'{bia}V')
                continue
            result_del_n_eff = fc.Transmission_fitting_n_eff_V(self.wave_len, self.I, n_eff, self.bias, bia)
            self.del_n_eff.append(result_del_n_eff[0])
            plt.plot(self.wave_len[self.bias.index(bia)],result_del_n_eff[1],linewidth=0.8,label=f'{bia}V')
        plt.xlabel('wavelength[nm]',fontdict=self.label_font_properties)
        plt.ylabel('intensity[W]',fontdict=self.label_font_properties)
        plt.title('Fitted Intensity Graph',fontdict=self.title_font_properties)
        plt.legend(loc='upper right',fontsize='8',ncol=2)
        plt.grid()
        plt.show()
    def del_n_eff_by_voltage(self):
        plt.plot(self.bias, self.del_n_eff, 'r-')
        plt.axhline(0, color='black',linestyle='dashed',linewidth=1)  # x축에 대한 수평선
        plt.axvline(0, color='black',linestyle='dashed',linewidth=1)  # y축에 대한 수직선
        plt.xlabel('voltage[V]', fontdict=self.label_font_properties)
        plt.ylabel(r'$\Delta$'+'n_eff', fontdict=self.label_font_properties)
        plt.title(r'$\Delta$'+'n_eff - Voltage Graph', fontdict=self.title_font_properties)
        plt.grid()
        plt.show()

# 예시 사용 방법
test = plot_TR('D08','20190526_082853','(0,0)')
test.data_parse()
test.fitted_TR_graph_plot()
test.del_n_eff_by_voltage()

  # -> 시도 방법 1 (극댓값 찾기)
'''
    trans_max=np.array([])
    wave_len_max=np.array([])
    for k in range(2, wave_len.shape[1]):
        if k == wave_len.shape[1] - 1:
            continue
        if trans[i][k] > trans[i][k - 1] and trans[i][k] < trans[i][k + 1]:
            trans_max = np.append(trans_max, trans[i][k])
            wave_len_max = np.append(wave_len_max, wave_len[i][k])
    print(trans_max.size, wave_len.shape[0])
    plt.plot(wave_len_max, trans_max, 'ro',markersize=0.5)
'''