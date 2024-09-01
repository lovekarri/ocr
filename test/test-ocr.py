
import json



def load_json_with_path(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        return f.read()
    

def get_anglevalue_from_path(file_path: str) -> float:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'result' in data and isinstance(data['result'], dict):
                if 'anglevalue' in data['result']:
                    return data['result']['anglevalue']
            return -1
    except FileNotFoundError:
        return -1
    except json.jsonDecodeError:
        return -1


def find_correct_angle(file_path: str) -> float:

    anglevalue = get_anglevalue_from_path(file_path)
    return anglevalue


def is_between(v, start, end, include_equal=True):
    # '''
    # >>> is_between(1, 1, 2)
    # True
    # >>> is_between(1, 1, 2, False)
    # False
    # >>> is_between(1, 6, 2)
    # False
    # >>> is_between(1, 6, 2, False)
    # False
    # '''
    '''
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_1.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_10.json'), 0.08,10.08)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_100.json'), 1.34,11.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_101.json'), 340.83,350.83)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_102.json'), 352.37,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_103.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_104.json'), 330.85,340.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_105.json'), 0,9.54)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_106.json'), 9.65,19.65)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_107.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_108.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_109.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_11.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_110.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_111.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_112.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_113.json'), 343.91,353.91)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_114.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_115.json'), 0,7.84)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_116.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_117.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_118.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_119.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_12.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_120.json'), 0,7.82)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_121.json'), 10.75,20.75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_122.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_123.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_124.json'), 0,9.9)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_125.json'), 322.65,332.65)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_126.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_127.json'), 75.88,85.88)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_13.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_130.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_131.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_132.json'), 0,7.74)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_133.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_134.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_135.json'), 90,100.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_136.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_137.json'), 348.66,358.66)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_138.json'), 0,8.04)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_14.json'), 352.4,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_140.json'), 0,6.29)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_141.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_142.json'), 350.91,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_144.json'), 346.47,356.47)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_145.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_146.json'), 347,357.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_148.json'), 0,7.36)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_149.json'), 3,13.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_15.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_150.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_151.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_152.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_153.json'), 348.6,358.6)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_154.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_156.json'), 0,9.72)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_157.json'), 349.81,359.81)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_158.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_159.json'), 1.19,11.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_16.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_160.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_161.json'), 8,18)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_162.json'), 351.48,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_163.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_164.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_165.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_166.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_167.json'), 1.98,11.98)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_168.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_169.json'), 351.0,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_17.json'), 0,7.96)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_171.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_172.json'), 345.23,355.23)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_173.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_174.json'), 265,275.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_175.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_176.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_177.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_178.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_18.json'), 0.49,10.49)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_180.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_181.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_182.json'), 268.27,278.27)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_183.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_184.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_186.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_187.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_188.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_189.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_19.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_190.json'), 0,8.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_191.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_192.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_193.json'), 2,12.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_194.json'), 352.4,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_195.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_196.json'), 175,185.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_197.json'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_198.json'), 95.8,105.8)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_199.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_2.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_20.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_200.json'), 2.06,12.06)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_201.json'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_202.json'), 38,48)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_203.json'), 93.92,103.92)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_204.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_205.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_206.json'), 0,6.33)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_207.json'), 348.25,358.25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_208.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_209.json'), 349.32,359.32)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_21.json'), 353.26,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_210.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_211.json'), 346.03,356.03)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_212.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_213.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_214.json'), 348.38,358.38)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_215.json'), 2.31,12.31)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_216.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_217.json'), 18.32,28.32)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_218.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_219.json'), 351.82,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_22.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_220.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_221.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_222.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_223.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_224.json'), 352.22,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_225.json'), 0,4.02)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_226.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_227.json'), 265,275.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_228.json'), 265,275.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_229.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_23.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_230.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_231.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_232.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_233.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_234.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_235.json'), 0,5.92)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_236.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_237.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_238.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_239.json'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_24.json'), 0,8.01)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_240.json'), 337.95,347.95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_241.json'), 341.07,351.07)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_242.json'), 70.82,80.82)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_243.json'), 70.82,80.82)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_244.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_245.json'), 349.4,359.4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_246.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_247.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_248.json'), 0,10.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_249.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_25.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_250.json'), 347.5,357.5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_251.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_252.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_253.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_254.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_255.json'), 351.19,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_256.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_257.json'), 350.6,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_258.json'), 0.64,10.64)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_259.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_26.json'), 82.34,92.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_260.json'), 0,7.2)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_261.json'), 2.31,12.31)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_262.json'), 353.93,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_263.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_264.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_265.json'), 350.26,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_266.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_267.json'), 0,8.62)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_268.json'), 344.76,354.76)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_269.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_27.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_270.json'), 342.01,352.01)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_271.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_272.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_273.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_274.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_275.json'), 0,9.51)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_276.json'), 352.9,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_277.json'), 84.09,94.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_278.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_279.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_28.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_280.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_281.json'), 84.19,94.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_282.json'), 0,9.18)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_283.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_284.json'), 351.08,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_285.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_286.json'), 1.34,11.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_287.json'), 3.47,13.47)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_288.json'), 271.57,281.57)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_289.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_29.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_290.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_291.json'), 175,185.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_292.json'), 20,30)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_293.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_294.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_295.json'), 83.19,93.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_296.json'), 83.75,93.75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_297.json'), 350.49,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_298.json'), 353.04,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_299.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_3.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_30.json'), 0,6.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_300.json'), 1.71,11.71)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_301.json'), 75,85.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_302.json'), 85,95.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_303.json'), 340,3505.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_304.json'), 85,95.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_305.json'), 338.34,348.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_306.json'), 255,265)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_307.json'), 275.08,285.08)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_308.json'), 0,6.22)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_309.json'), 0,7.39)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_31.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_310.json'), 350.36,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_311.json'), 351,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_312.json'), 65,75.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_313.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_314.json'), 265.88,275.88)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_315.json'), 265.88,275.88)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_316.json'), 325,335)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_317.json'), 80,90.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_318.json'), 20.41,30.41)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_319.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_32.json'), 353.51,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_320.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_321.json'), 353.89,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_322.json'), 0,6.47)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_323.json'), 15,25.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_324.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_325.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_326.json'), 308.25,318.25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_327.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_328.json'), 352.1,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_329.json'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_33.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_330.json'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_331.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_332.json'), 352.11,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_333.json'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_334.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_335.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_336.json'), 0,9.33)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_337.json'), 83.68,93.68)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_338.json'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_339.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_34.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_340.json'), 0.78,10.78)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_341.json'), 349.81,359.81)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_342.json'), 2.99,12.99)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_343.json'), 1.01,11.01)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_344.json'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_345.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_346.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_347.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_348.json'), 77.06,87.06)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_349.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_35.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_350.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_351.json'), 344.99,354.99)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_352.json'), 0,8.62)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_353.json'), 15.49,25.49)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_354.json'), 10.22,20.22)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_355.json'), 328.43,338.43)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_356.json'), 265.13,275.13)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_357.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_358.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_359.json'), 350.86,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_36.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_360.json'), 77.21,87.21)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_361.json'), 304.77,314.77)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_362.json'), 348.96,358.96)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_363.json'), 1,11.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_364.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_365.json'), 0,9.82)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_366.json'), 0,10.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_367.json'), 0.36,10.36)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_368.json'), 0,8.07)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_369.json'), 335.56,345.56)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_37.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_370.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_371.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_372.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_373.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_374.json'), 0,7.31)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_375.json'), 353.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_376.json'), 342.44,352.44)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_377.json'), 346.25,356.25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_378.json'), 348.77,358.77)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_379.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_38.json'), 9.25,19.25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_380.json'), 13.0,23.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_381.json'), 7.31,17.31)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_382.json'), 6.8,16.8)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_383.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_384.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_385.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_386.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_387.json'), 5.3,15.3)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_388.json'), 6.04,16.04)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_389.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_39.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_390.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_391.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_392.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_393.json'), 341.2,351.2)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_394.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_395.json'), 8.67,18.67)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_396.json'), 47.57,57.57)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_397.json'), 350.68,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_398.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_399.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_4.json'), 345.0,355.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_40.json'), 0,8.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_400.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_401.json'), 352.99,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_402.json'), 328.08,338.08)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_403.json'), 7.26,17.26)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_404.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_405.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_406.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_407.json'), 0.88,10.88)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_408.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_409.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_41.json'), 266.58,276.58)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_410.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_411.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_412.json'), 342.2,352.2)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_413.json'), 0,7.1)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_414.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_415.json'), 80.79,90.79)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_416.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_417.json'), 4.87,14.87)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_418.json'), 4.21,14.21)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_419.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_42.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_420.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_421.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_422.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_423.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_424.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_426.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_427.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_428.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_429.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_43.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_430.json'), 5.38,15.38)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_431.json'), 349.37,359.37)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_433.json'), 352.69,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_434.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_435.json'), 353.19,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_436.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_439.json'), 353.13,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_44.json'), 0.57,10.57)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_440.json'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_441.json'), 348.16,358.16)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_442.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_444.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_445.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_446.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_447.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_448.json'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_449.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_45.json'), 0,7.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_450.json'), 0,8.99)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_452.json'), 8.84,18.84)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_453.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_455.json'), 343.11,353.11)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_459.json'), 0,9.89)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_46.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_462.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_463.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_465.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_468.json'), 5.01,15.01)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_47.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_471.json'), 2.77,12.77)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_472.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_477.json'), 56.44,66.44)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_48.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_482.json'), 277.26,287.26)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_483.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_486.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_49.json'), 3.25,13.25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_491.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_492.json'), 353.21,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_494.json'), 0,8.37)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_496.json'), 0,8.04)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_497.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_499.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_5.json'), 281.0,291.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_50.json'), 343.21,353.21)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_503.json'), 351.37,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_504.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_506.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_507.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_51.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_513.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_514.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_516.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_518.json'), 346.75,356.75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_519.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_52.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_522.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_525.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_526.json'), 348.09,358.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_529.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_53.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_530.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_533.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_534.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_536.json'), 353.28,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_538.json'), 1.46,11.46)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_54.json'), 340.38,350.38)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_543.json'), 351.35,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_545.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_547.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_55.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_551.json'), 353.08,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_555.json'), 297.84,307.84)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_556.json'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_557.json'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_56.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_560.json'), 13.9,23.9)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_561.json'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_562.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_563.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_564.json'), 15,25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_565.json'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_566.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_567.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_568.json'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_569.json'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_57.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_571.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_572.json'), 351.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_573.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_574.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_575.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_576.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_577.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_578.json'), 325,335)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_579.json'), 347,357)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_58.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_580.json'), 0,9.3)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_581.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_582.json'), 13,23)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_583.json'), 14.5,24.5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_584.json'), 109,119)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_585.json'), 118,128)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_586.json'), 138,148)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_587.json'), 87,97)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_588.json'), 350,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_589.json'), 350,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_59.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_590.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_591.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_592.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_593.json'), 344.85,354.85)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_594.json'), 0,8.56)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_595.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_596.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_597.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_598.json'), 105,115)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_599.json'), 105,115)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_6.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_60.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_600.json'), 105,115)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_601.json'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_602.json'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_603.json'), 351.02,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_604.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_605.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_606.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_607.json'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_608.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_609.json'), 105,115)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_61.json'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_610.json'), 340,350)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_611.json'), 345,355)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_612.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_613.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_614.json'), 337,347)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_615.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_616.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_617.json'), 337,347)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_618.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_619.json'), 347,357)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_62.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_620.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_621.json'), 0.84,10.84)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_63.json'), 348.5,358.5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_64.json'), 352.16,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_65.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_66.json'), 347.01,357.01)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_67.json'), 0,6.75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_68.json'), 343.91,353.91)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_69.json'), 268.18,278.18)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_7.json'), 344.22,354.22)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_70.json'), 0,7.39)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_71.json'), 0,6.33)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_72.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_73.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_74.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_75.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_76.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_77.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_78.json'), 0,4.38)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_79.json'), 30.87,40.87)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_8.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_80.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_81.json'), 25.96,35.96)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_82.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_83.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_84.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_85.json'), 346.47,356.47)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_86.json'), 351.63,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_87.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_88.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_89.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_9.json'), 352.23,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_90.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_91.json'), 82.85,92.85)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_92.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_93.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_94.json'), 6.82,16.82)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_95.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_96.json'), 351.27,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_97.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_98.json'), 0,9.72)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_99.json'), 348.29,358.29)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_1.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_10.json'), 0,7.45)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_100.json'), 20,30)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_101.json'), 351.49,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_102.json'), 353.22,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_104.json'), 25,35)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_105.json'), 267.0,277.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_106.json'), 351.59,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_107.json'), 175,185)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_108.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_109.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_11.json'), 0,6.44)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_110.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_111.json'), 80,90)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_112.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_113.json'), 205,215)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_114.json'), 250,260)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_115.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_116.json'), 350,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_117.json'), 340,350)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_118.json'), 0,7.58)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_119.json'), 343.94,353.94)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_12.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_120.json'), 6.77,16.77)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_121.json'), 175,185)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_122.json'), 351.39,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_123.json'), 351.05,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_124.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_125.json'), 0,7.69)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_126.json'), 309.29,319.29)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_127.json'), 325,335)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_128.json'), 0,6.57)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_129.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_13.json'), 325.19,335.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_130.json'), 0,6.99)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_131.json'), 349.74,359.74)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_132.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_133.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_134.json'), 353.59,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_135.json'), 352.71,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_136.json'), 185,195)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_137.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_138.json'), 0,6.53)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_139.json'), 0,6.29)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_14.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_140.json'), 0,4.01)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_141.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_142.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_143.json'), 75,85)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_144.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_145.json'), 351.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_146.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_147.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_148.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_149.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_15.json'), 3.62,13.62)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_150.json'), 260,270)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_151.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_152.json'), 353.57,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_153.json'), 351.39,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_154.json'), 0,6.79)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_155.json'), 0,6.08)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_156.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_157.json'), 6.61,16.61)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_158.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_159.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_16.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_160.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_161.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_162.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_163.json'), 35,45)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_164.json'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_165.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_166.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_167.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_168.json'), 315,325)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_169.json'), 255,265)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_17.json'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_170.json'), 1.22,11.22)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_171.json'), 6.75,16.75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_172.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_173.json'), 350.65,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_174.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_175.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_176.json'), 0,7.66)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_177.json'), 282.68,292.68)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_178.json'), 2.05,12.05)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_179.json'), 0.1,10.1)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_18.json'), 65,75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_180.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_181.json'), 351.02,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_182.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_183.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_184.json'), 352.9,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_185.json'), 0,6.35)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_186.json'), 0,7.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_187.json'), 0,7.7)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_188.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_189.json'), 2.34,12.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_19.json'), 349.81,359.81)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_190.json'), 305,315)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_191.json'), 305,315)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_192.json'), 7.71,17.71)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_193.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_194.json'), 3.03,13.03)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_195.json'), 79.14,89.14)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_196.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_197.json'), 160,170)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_198.json'), 45,55)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_199.json'), 347.64,357.64)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_2.json'), 0,7.69)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_20.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_200.json'), 352.12,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_201.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_202.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_203.json'), 0,6.6)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_204.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_205.json'), 0,9.55)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_206.json'), 275.78,285.78)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_207.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_208.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_209.json'), 0.06,10.06)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_21.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_210.json'), 83.89,93.89)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_211.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_212.json'), 353.85,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_213.json'), 344.05,354.05)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_214.json'), 313.68,323.68)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_215.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_216.json'), 82.5,92.5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_217.json'), 15,25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_218.json'), 0,5.93)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_219.json'), 0,8.96)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_22.json'), 0,5.83)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_220.json'), 0,7.63)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_221.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_222.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_223.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_224.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_225.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_226.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_227.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_228.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_229.json'), 0,6.85)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_23.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_230.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_231.json'), 1.05,11.05)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_232.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_233.json'), 350.64,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_234.json'), 0,7.43)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_235.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_236.json'), 180,190)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_237.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_238.json'), 270,280)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_239.json'), 0,7.12)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_24.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_240.json'), 0,10)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_241.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_242.json'), 348.29,358.29)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_243.json'), 10.21,20.21)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_244.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_245.json'), 65,75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_246.json'), 1.57,11.57)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_247.json'), 0,6.9)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_248.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_249.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_25.json'), 339.58,349.58)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_250.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_251.json'), 0,5.77)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_252.json'), 0,7.96)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_253.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_254.json'), 0,7.86)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_255.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_256.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_257.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_258.json'), 0,7.75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_259.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_26.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_260.json'), 353.89,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_261.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_262.json'), 0,9.86)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_263.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_264.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_265.json'), 29.26,39.26)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_266.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_267.json'), 0,5.93)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_268.json'), 346.67,356.67)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_269.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_27.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_270.json'), 0,7.9)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_271.json'), 351.09,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_272.json'), 83.21,93.21)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_273.json'), 0,9.57)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_274.json'), 6.08,16.08)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_275.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_276.json'), 0,5.87)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_277.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_278.json'), 8.85,18.85)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_279.json'), 8.28,18.28)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_28.json'), 0,7.11)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_280.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_281.json'), 350.72,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_282.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_283.json'), 261,271)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_284.json'), 175,185)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_285.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_286.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_287.json'), 255,265)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_288.json'), 0,6.95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_289.json'), 352.76,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_29.json'), 352.88,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_290.json'), 35,45)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_291.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_292.json'), 351.29,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_293.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_294.json'), 353.87,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_295.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_296.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_297.json'), 0,8.26)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_298.json'), 80,90)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_299.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_3.json'), 352.61,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_30.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_300.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_301.json'), 3.13,13.13)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_302.json'), 170,180)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_303.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_304.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_305.json'), 255,265)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_306.json'), 0,8.15)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_307.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_308.json'), 5.71,15.71)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_309.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_31.json'), 0,6.29)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_310.json'), 0,6.31)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_311.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_312.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_313.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_314.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_315.json'), 0,9.86)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_316.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_317.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_318.json'), 285,295)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_319.json'), 1,11)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_32.json'), 0,10)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_320.json'), 352.55,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_321.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_322.json'), 0,6.62)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_323.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_324.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_325.json'), 10.71,20.71)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_326.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_327.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_328.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_329.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_33.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_330.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_331.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_332.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_333.json'), 0,5.89)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_334.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_335.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_336.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_337.json'), 352.5,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_338.json'), 350,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_339.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_34.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_340.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_341.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_342.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_343.json'), 0,8.5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_344.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_345.json'), 353.14,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_346.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_347.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_348.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_35.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_350.json'), 350.31,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_351.json'), 1.71,11.71)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_352.json'), 353.3,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_354.json'), 40,50)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_355.json'), 0,5.92)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_356.json'), 347,357)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_357.json'), 0,8)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_36.json'), 351.86,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_360.json'), 353.5,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_361.json'), 55,65)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_362.json'), 0,6.68)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_363.json'), 0,4.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_365.json'), 345,355)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_366.json'), 351.84,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_368.json'), 5,15)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_37.json'), 0,4.43)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_372.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_373.json'), 347,357)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_38.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_380.json'), 60,70)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_384.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_389.json'), 0,7.64)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_39.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_391.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_392.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_397.json'), 353.13,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_399.json'), 325,335)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_4.json'), 1.77,11.77)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_40.json'), 65,75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_401.json'), 2.13,12.13)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_404.json'), 351.86,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_407.json'), 353.39,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_41.json'), 0,6.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_42.json'), 0,6.86)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_421.json'), 351.63,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_427.json'), 0,9.46)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_43.json'), 352.21,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_434.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_44.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_440.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_442.json'), 83.97,93.97)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_445.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_45.json'), 337,347)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_452.json'), 352.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_455.json'), 5,15)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_46.json'), 8.39,18.39)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_464.json'), 348.08,358.08)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_47.json'), 3.6,13.6)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_472.json'), 0,8.62)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_475.json'), 335,345)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_476.json'), 325,335)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_477.json'), 268.06,278.06)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_478.json'), 351.84,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_479.json'), 11.63,21.63)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_48.json'), 342.17,352.17)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_480.json'), 330.51,340.51)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_481.json'), 343,353)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_49.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_5.json'), 345.13,355.13)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_50.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_51.json'), 280.46,290.46)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_52.json'), 349.06,359.06)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_53.json'), 352.49,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_54.json'), 351.23,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_55.json'), 15.04,25.04)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_56.json'), 21,31)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_57.json'), 0,6.24)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_58.json'), 40,50)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_59.json'), 0,7.73)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_6.json'), 0,6.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_60.json'), 0,7.45)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_61.json'), 352.51,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_62.json'), 5,15)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_63.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_67.json'), 352.69,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_68.json'), 7.76,17.76)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_69.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_7.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_70.json'), 353.97,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_72.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_73.json'), 0,6.75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_74.json'), 352.75,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_75.json'), 82.33,92.33)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_76.json'), 0,10)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_77.json'), 0,10)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_79.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_8.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_80.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_81.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_82.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_83.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_85.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_86.json'), 0,5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_87.json'), 0,9.57)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_88.json'), 351.35,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_9.json'), 0,8.51)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_90.json'), 15,25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_91.json'), 33.66,43.66)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_92.json'), 0,9.33)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_94.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_95.json'), 33.33,43.33)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_96.json'), 352.83,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_97.json'), 0,6.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_sugar_99.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_1.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_10.json'), 0.08,10.08)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_100.json'), 1.34,11.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_101.json'), 348.83,358.83)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_102.json'), 352.37,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_103.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_104.json'), 351.85,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_105.json'), 0,9.54)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_106.json'), 9.65,19.65)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_107.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_108.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_109.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_11.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_110.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_111.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_112.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_113.json'), 343.91,353.91)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_114.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_115.json'), 0,7.84)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_116.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_117.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_118.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_119.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_12.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_120.json'), 0,7.82)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_121.json'), 3.75,13.75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_122.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_123.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_124.json'), 0,9.9)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_125.json'), 327.65,337.65)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_126.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_127.json'), 75.88,85.88)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_13.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_130.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_131.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_132.json'), 0,7.74)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_133.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_134.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_135.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_136.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_137.json'), 348.66,358.66)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_138.json'), 0,8.04)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_14.json'), 352.4,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_140.json'), 0,6.29)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_141.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_142.json'), 350.91,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_144.json'), 346.47,356.47)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_145.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_146.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_148.json'), 0,7.36)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_149.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_15.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_150.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_151.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_152.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_153.json'), 348.6,358.6)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_154.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_156.json'), 0,9.72)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_157.json'), 349.81,359.81)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_158.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_159.json'), 1.19,11.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_16.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_160.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_161.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_162.json'), 351.48,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_163.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_164.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_165.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_166.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_167.json'), 1.98,11.98)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_168.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_169.json'), 351.0,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_17.json'), 0,7.96)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_171.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_172.json'), 345.23,355.23)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_173.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_174.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_175.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_176.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_177.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_178.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_18.json'), 0.49,10.49)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_180.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_181.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_182.json'), 82.27,92.27)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_183.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_184.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_186.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_187.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_188.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_189.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_19.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_190.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_191.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_192.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_193.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_194.json'), 352.4,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_195.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_196.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_197.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_198.json'), 277.8,287.8)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_199.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_2.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_20.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_200.json'), 2.06,12.06)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_201.json'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_202.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_203.json'), 273.92,283.92)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_204.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_205.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_206.json'), 0,6.33)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_207.json'), 348.25,358.25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_208.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_209.json'), 349.32,359.32)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_21.json'), 353.26,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_210.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_211.json'), 346.03,356.03)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_212.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_213.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_214.json'), 348.38,358.38)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_215.json'), 2.31,12.31)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_216.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_217.json'), 9.32,19.32)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_218.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_219.json'), 351.82,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_22.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_220.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_221.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_222.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_223.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_224.json'), 352.22,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_225.json'), 0,4.02)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_226.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_227.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_228.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_229.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_23.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_230.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_231.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_232.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_233.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_234.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_235.json'), 0,5.92)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_236.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_237.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_238.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_239.json'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_24.json'), 0,8.01)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_240.json'), 344.95,354.95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_241.json'), 341.07,351.07)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_242.json'), 58.82,68.82)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_243.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_244.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_245.json'), 349.4,359.4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_246.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_247.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_248.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_249.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_25.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_250.json'), 347.5,357.5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_251.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_252.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_253.json'), 45,55)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_254.json'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_255.json'), 351.19,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_256.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_257.json'), 350.6,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_258.json'), 0.64,10.64)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_259.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_26.json'), 268.34,278.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_260.json'), 0,7.2)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_261.json'), 2.31,12.31)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_262.json'), 353.93,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_263.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_264.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_265.json'), 350.26,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_266.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_267.json'), 0,8.62)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_268.json'), 344.76,354.76)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_269.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_27.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_270.json'), 342.01,352.01)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_271.json'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_272.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_273.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_274.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_275.json'), 0,9.51)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_276.json'), 352.9,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_277.json'), 84.09,94.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_278.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_279.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_28.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_280.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_281.json'), 350.19,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_282.json'), 342,252.18)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_283.json'), 85,95.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_284.json'), 351.08,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_285.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_286.json'), 1.34,11.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_287.json'), 3.47,13.47)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_288.json'), 271.57,281.57)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_289.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_29.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_290.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_291.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_292.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_293.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_294.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_295.json'), 58.19,68.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_296.json'), 83.75,93.75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_297.json'), 350.49,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_298.json'), 353.04,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_299.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_3.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_30.json'), 0,6.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_300.json'), 1.71,11.71)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_301.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_302.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_303.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_304.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_305.json'), 338.34,348.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_306.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_307.json'), 334.08,344.08)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_308.json'), 0,6.22)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_309.json'), 0,7.39)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_31.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_310.json'), 350.36,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_311.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_312.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_313.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_314.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_315.json'), 348.88,358.88)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_316.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_317.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_318.json'), 14.41,24.41)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_319.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_32.json'), 353.51,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_320.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_321.json'), 353.89,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_322.json'), 0,6.47)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_323.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_324.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_325.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_326.json'), 319.25,329.25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_327.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_328.json'), 352.1,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_329.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_33.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_330.json'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_331.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_332.json'), 352.11,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_333.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_334.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_335.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_336.json'), 0,9.33)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_337.json'), 83.68,93.68)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_338.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_339.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_34.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_340.json'), 0.78,10.78)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_341.json'), 349.81,359.81)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_342.json'), 2.99,12.99)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_343.json'), 1.01,11.01)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_344.json'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_345.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_346.json'), 350,360.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_347.json'), 85,95)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_348.json'), 77.06,87.06)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_349.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_35.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_350.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_351.json'), 344.99,354.99)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_352.json'), 0,8.62)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_353.json'), 0.49,10.49)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_354.json'), 2.22,12.22)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_355.json'), 328.43,338.43)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_356.json'), 83.13,93.13)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_357.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_358.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_359.json'), 350.86,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_36.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_360.json'), 77.21,87.21)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_361.json'), 304.77,314.77)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_362.json'), 348.96,358.96)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_363.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_364.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_365.json'), 0,9.82)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_366.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_367.json'), 0.36,10.36)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_368.json'), 0,8.07)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_369.json'), 340.56,350.56)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_37.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_370.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_371.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_372.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_373.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_374.json'), 0,7.31)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_375.json'), 353.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_376.json'), 342.44,352.44)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_377.json'), 346.25,356.25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_378.json'), 348.77,358.77)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_379.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_38.json'), 17.25,27.25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_380.json'), 20.0,30.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_381.json'), 20.31,30.31)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_382.json'), 6.8,16.8)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_383.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_384.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_385.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_386.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_387.json'), 13.5,23.5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_388.json'), 12.5,22.5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_389.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_39.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_390.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_391.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_392.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_393.json'), 330.2,340.2)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_394.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_395.json'), 25,35)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_396.json'), 47.57,57.57)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_397.json'), 350.68,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_398.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_399.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_4.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_40.json'), 0,8.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_400.json'), 340,350)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_401.json'), 352.99,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_402.json'), 315.08,325.08)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_403.json'), 30,40)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_404.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_405.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_406.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_407.json'), 0.88,10.88)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_408.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_409.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_41.json'), 266.58,276.58)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_410.json'), 345,355)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_411.json'), 265,275)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_412.json'), 335.2,345.2)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_413.json'), 0,7.1)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_414.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_415.json'), 90.79,100.79)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_416.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_417.json'), 4.87,14.87)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_418.json'), 4.21,14.21)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_419.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_42.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_420.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_421.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_422.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_423.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_424.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_426.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_427.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_428.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_429.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_43.json'), 0,10.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_430.json'), 5.38,15.38)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_431.json'), 349.37,359.37)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_433.json'), 352.69,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_434.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_435.json'), 353.19,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_436.json'),330,340)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_439.json'), 353.13,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_44.json'), 0.57,10.57)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_440.json'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_441.json'), 348.16,358.16)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_442.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_444.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_445.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_446.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_447.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_448.json'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_449.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_45.json'), 0,7.34)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_450.json'), 0,8.99)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_452.json'), 8.84,18.84)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_453.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_455.json'), 343.11,353.11)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_459.json'), 0,9.89)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_46.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_462.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_463.json'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_465.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_468.json'), 88,98)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_47.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_471.json'), 2.77,12.77)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_472.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_477.json'), 56.44,66.44)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_48.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_482.json'), 100,110)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_483.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_486.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_49.json'), 3.25,13.25)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_491.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_492.json'), 353.21,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_494.json'), 0,8.37)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_496.json'), 0,8.04)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_497.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_499.json'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_5.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_50.json'), 343.21,353.21)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_503.json'), 351.37,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_504.json'), 3.43,13.43)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_506.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_507.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_51.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_513.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_514.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_516.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_518.json'), 346.75,356.75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_519.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_52.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_522.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_525.json'), 340,350)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_526.json'), 348.09,358.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_529.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_53.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_530.json'), 90,100)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_533.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_534.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_536.json'), 353.28,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_538.json'), 1.46,11.46)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_54.json'), 65,75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_543.json'), 351.35,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_545.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_547.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_55.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_551.json'), 353.08,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_555.json'), 297.84,307.84)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_556.json'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_557.json'), 353.7,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_56.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_560.json'), 13.9,23.9)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_561.json'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_562.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_563.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_564.json'), 2.59,12.59)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_565.json'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_566.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_567.json'), 0,4)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_568.json'), 4.09,14.09)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_569.json'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_57.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_571.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_572.json'), 351.34,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_573.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_574.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_575.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_576.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_577.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_578.json'), 346.47,356.47)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_579.json'), 0,4.22)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_58.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_580.json'), 0,9.3)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_581.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_582.json'), 8.57,18.57)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_583.json'), 9.45,19.45)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_584.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_585.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_586.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_587.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_588.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_589.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_59.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_590.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_591.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_592.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_593.json'), 344.85,354.85)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_594.json'), 0,8.56)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_595.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_596.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_597.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_598.json'), 274.67,284.67)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_599.json'), 279.04,289.04)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_6.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_60.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_600.json'), 353.8,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_601.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_602.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_603.json'), 351.02,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_604.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_605.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_606.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_607.json'), 0,8.61)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_608.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_609.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_61.json'), 0.19,10.19)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_610.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_611.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_612.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_613.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_614.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_615.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_616.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_617.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_618.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_619.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_62.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_620.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_621.json'), 0.84,10.84)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_63.json'), 348.5,358.5)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_64.json'), 352.16,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_65.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_66.json'), 330.01,340.01)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_67.json'), 0,6.75)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_68.json'), 327.91,337.91)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_69.json'), 337.18,347.18)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_7.json'), 344.22,354.22)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_70.json'), 0,7.39)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_71.json'), 0,6.33)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_72.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_73.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_74.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_75.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_76.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_77.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_78.json'), 0,4.38)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_79.json'), 35.87,45.87)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_8.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_80.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_81.json'), 30.96,40.96)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_82.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_83.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_84.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_85.json'), 346.47,356.47)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_86.json'), 351.63,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_87.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_88.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_89.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_9.json'), 352.23,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_90.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_91.json'), 82.85,92.85)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_92.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_93.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_94.json'), 6.82,16.82)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_95.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_96.json'), 351.27,360)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_97.json'), 0,5.0)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_98.json'), 0,9.72)
    True
    >>> is_between(find_correct_angle('/paddle/images/ocr/json/blood_pressure_99.json'), 345.29,355.29)
    True
    '''
    if include_equal:
        return v <= max(start, end) and v >= min(start, end)
    return v < max(start, end) and v > min(start, end)



if __name__ == '__main__':
    import doctest
    print(doctest.testmod(verbose=False, report=False))