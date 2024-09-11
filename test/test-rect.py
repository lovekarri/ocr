import os
import json


def get_rect_from_path(file_path: str) -> float:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'output' in data and isinstance(data['output'], dict):
                if 'rect' in data['output']:
                    return data['output']['rect']
            return None
    except FileNotFoundError:
        return None
    except json.jsonDecodeError:
        return None
    


def find_correct_rect(file_path: str) -> float:

    rect = get_rect_from_path(file_path)
    return rect


def is_json(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    return extension in ['.json']


def is_between(v, start, end, include_equal=True):
    
    '''
    >>> is_between(find_correct_rect('contours_json/blood_pressure_620.json'), ((761.51, 1319.2), (383.62, 511.86)),((771.51, 1329.2), (393.62, 521.86)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_270.json'), ((432.02, 111.42), (195.23, 244.98)),((442.02, 121.42), (205.23, 254.98)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_2.json'),   
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_362.json'), ((869.11, 743.99), (116.08, 161.17)),((879.11, 753.99), (126.08, 171.17)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_49.json'), ((404.44, 538.64), (454.56, 542.13)),((414.44, 548.64), (464.56, 552.13)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_374.json'), ((283.11, 415.71), (301.82, 382.68)),((293.11, 425.71), (311.82, 392.68)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_231.json'), ((707.96, 1482.69), (725.39, 1065.31)),((717.96, 1492.69), (735.39, 1075.31)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_73.json'), ((406.0, 589.5), (448.0, 381.0)),((416.0, 599.5), (458.0, 391.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_358.json'), ((272.85, 175.72), (212.52, 152.28)),((282.85, 185.72), (222.52, 162.28)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_421.json'), ((283.5, 353.5), (296.0, 224.0)),((293.5, 363.5), (306.0, 234.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_564.json'), ((620.56, 712.79), (231.46, 272.07)),((630.56, 722.79), (241.46, 282.07)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_134.json'), ((164.15, 602.54), (239.73, 195.93)),((174.15, 612.54), (249.73, 205.93)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_24.json'), ((310.19, 272.02), (220.35, 274.9)),((320.19, 282.02), (230.35, 284.9)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_163.json'), ((340.19, 413.83), (638.78, 684.16)),((350.19, 423.83), (648.78, 694.16)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_65.json'), ((494.93, 434.88), (412.01, 505.78)),((504.93, 444.88), (422.01, 515.78)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_122.json'), ((470.0, 591.5), (430.0, 357.0)),((480.0, 601.5), (440.0, 367.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_572.json'), ((407.14, 488.79), (691.28, 510.05)),((417.14, 498.79), (701.28, 520.05)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_440.json'), ((433.5, 669.02), (378.33, 424.91)),((443.5, 679.02), (388.33, 434.91)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_339.json'), ((379.5, 949.5), (618.0, 514.0)),((389.5, 959.5), (628.0, 524.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_12.json'), ((445.96, 421.31), (504.17, 563.99)),((455.96, 431.31), (514.17, 573.99)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_417.json'), ((649.81, 812.35), (231.98, 284.45)),((659.81, 822.35), (241.98, 294.45)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_45.json'), ((657.81, 308.72), (604.92, 549.42)),((667.81, 318.72), (614.92, 559.42)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_544.json'), ((161.62, 85.72), (115.61, 69.91)),((171.62, 95.72), (125.61, 79.91)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_114.json'), ((382.5, 802.5), (202.0, 254.0)),((392.5, 812.5), (212.0, 264.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_401.json'), ((380.94, 659.53), (791.95, 613.99)),((390.94, 669.53), (801.95, 623.99)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_53.json'), ((444.92, 446.14), (225.51, 276.95)),((454.92, 456.14), (235.51, 286.95)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_378.json'), ((626.41, 738.12), (274.15, 252.42)),((636.41, 748.12), (284.15, 262.42)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_397.json'), ((353.38, 707.34), (448.74, 331.33)),((363.38, 717.34), (458.74, 341.33)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_513.json'), ((364.5, 539.0), (545.0, 602.0)),((374.5, 549.0), (555.0, 612.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_138.json'), ((657.61, 308.74), (605.15, 549.26)),((667.61, 318.74), (615.15, 559.26)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_568.json'), ((525.57, 578.26), (432.97, 498.43)),((535.57, 588.26), (442.97, 508.43)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_211.json'), ((483.65, 591.48), (398.88, 549.6)),((493.65, 601.48), (408.88, 559.6)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_180.json'), ((805.5, 309.5), (452.0, 336.0)),((815.5, 319.5), (462.0, 346.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_495.json'), ((224.25, 82.67), (67.0, 87.64)),((234.25, 92.67), (77.0, 97.64)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_246.json'), ((463.09, 616.37), (454.34, 630.66)),((473.09, 626.37), (464.34, 640.66)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_616.json'), ((563.64, 1072.35), (666.39, 933.16)),((573.64, 1082.35), (676.39, 943.16)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_28.json'), ((355.5, 391.5), (424.0, 492.0)),((365.5, 401.5), (434.0, 502.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_483.json'), ((457.0, 550.5), (630.0, 465.0)),((467.0, 560.5), (640.0, 475.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_529.json'), ((311.08, 591.75), (568.88, 715.98)),((321.08, 601.75), (578.88, 725.98)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_600.json'), ((625.7, 1758.6), (731.43, 565.48)),((635.7, 1768.6), (741.43, 575.48)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_250.json'), ((459.12, 673.84), (512.04, 713.7)),((469.12, 683.84), (522.04, 723.7)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_591.json'), ((345.82, 1046.33), (567.35, 536.63)),((355.82, 1056.33), (577.35, 546.63)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_207.json'), ((425.61, 985.82), (396.18, 569.19)),((435.61, 995.82), (406.18, 579.19)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_86.json'), ((414.19, 507.79), (486.83, 402.89)),((424.19, 517.79), (496.83, 412.89)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_69.json'), ((505.4, 692.25), (155.12, 191.98)),((515.4, 702.25), (165.12, 201.98)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_206.json'), ((531.58, 844.21), (1012.2, 708.4)),((541.58, 854.21), (1022.2, 718.4)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_87.json'), ((237.54, 521.25), (287.75, 235.14)),((247.54, 531.25), (297.75, 245.14)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_590.json'), ((392.65, 1087.15), (585.76, 526.04)),((402.65, 1097.15), (595.76, 536.04)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_601.json'), ((641.93, 1829.0), (713.92, 574.72)),((651.93, 1839.0), (723.92, 584.72)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_314.json'), ((642.4, 868.16), (599.14, 464.04)),((652.4, 878.16), (609.14, 474.04)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_197.json'), ((154.25, 390.86), (140.69, 193.51)),((164.25, 400.86), (150.69, 203.51)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_178.json'), ((418.5, 610.5), (462.0, 354.0)),((428.5, 620.5), (472.0, 364.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_482.json'), ((367.17, 587.23), (411.88, 336.75)),((377.17, 597.23), (421.88, 346.75)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_247.json'), ((474.35, 1532.51), (582.52, 400.86)),((484.35, 1542.51), (592.52, 410.86)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_617.json'), ((458.84, 1351.2), (263.53, 374.34)),((468.84, 1361.2), (273.53, 384.34)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_29.json'), ((290.5, 583.5), (568.0, 474.0)),((300.5, 593.5), (578.0, 484.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_302.json'), ((630.21, 527.98), (745.98, 538.13)),((640.21, 537.98), (755.98, 548.13)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_181.json'), ((460.59, 461.4), (431.45, 354.24)),((470.59, 471.4), (441.45, 364.24)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_494.json'), ((228.16, 481.9), (243.31, 317.11)),((238.16, 491.9), (253.31, 327.11)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_91.json'), ((595.33, 743.99), (226.72, 316.54)),((605.33, 753.99), (236.72, 326.54)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_210.json'), ((537.98, 811.47), (381.85, 536.5)),((547.98, 821.47), (391.85, 546.5)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_569.json'), ((433.5, 669.02), (378.33, 424.91)),((443.5, 679.02), (388.33, 434.91)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_457.json'), ((1050.92, 354.99), (283.63, 137.99)),((1060.92, 364.99), (293.63, 147.99)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_52.json'), ((430.42, 468.62), (330.15, 267.89)),((440.42, 478.62), (340.15, 277.89)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_379.json'), ((320.0, 661.0), (687.0, 555.0)),((330.0, 671.0), (697.0, 565.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_396.json'), ((549.64, 998.89), (153.08, 228.22)),((559.64, 1008.89), (163.08, 238.22)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_545.json'), ((485.68, 549.0), (463.64, 380.29)),((495.68, 559.0), (473.64, 390.29)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_115.json'), ((437.94, 481.08), (484.69, 593.59)),((447.94, 491.08), (494.69, 603.59)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_44.json'), ((407.62, 524.18), (455.61, 571.39)),((417.62, 534.18), (465.61, 581.39)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_380.json'), ((781.0, 331.0), (178.36, 261.54)),((791.0, 341.0), (188.36, 271.54)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_103.json'), ((365.28, 575.5), (503.16, 662.02)),((375.28, 585.5), (513.16, 672.02)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_416.json'), ((452.65, 768.37), (450.55, 345.31)),((462.65, 778.37), (460.55, 355.31)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_338.json'), ((696.82, 826.67), (281.77, 202.39)),((706.82, 836.67), (291.77, 212.39)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_504.json'), ((314.5, 528.0), (147.0, 134.0)),((324.5, 538.0), (157.0, 144.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_154.json'), ((413.79, 600.95), (379.33, 501.91)),((423.79, 610.95), (389.33, 511.91)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_436.json'), ((212.57, 599.52), (205.87, 162.94)),((222.57, 609.52), (215.87, 172.94)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_123.json'), ((408.68, 561.96), (554.22, 729.21)),((418.68, 571.96), (564.22, 739.21)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_573.json'), ((226.5, 282.5), (178.0, 234.0)),((236.5, 292.5), (188.0, 244.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_64.json'), ((312.65, 556.54), (462.27, 378.37)),((322.65, 566.54), (472.27, 388.37)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_524.json'), ((76.77, 108.31), (58.24, 28.47)),((86.77, 118.31), (68.24, 38.47)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_174.json'), ((256.5, 512.5), (230.0, 314.0)),((266.5, 522.5), (240.0, 324.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_33.json'), ((466.64, 516.41), (647.69, 620.13)),((476.64, 526.41), (657.69, 630.13)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_477.json'), ((742.99, 465.01), (361.46, 465.71)),((752.99, 475.01), (371.46, 475.71)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_25.json'), ((331.62, 434.62), (484.99, 616.68)),((341.62, 444.62), (494.99, 626.68)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_420.json'), ((277.86, 541.27), (352.11, 457.91)),((287.86, 551.27), (362.11, 467.91)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_565.json'), ((525.57, 578.26), (432.97, 498.43)),((535.57, 588.26), (442.97, 508.43)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_135.json'), ((501.8, 585.18), (483.49, 359.54)),((511.8, 595.18), (493.49, 369.54)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_72.json'), ((377.14, 539.08), (288.52, 342.34)),((387.14, 549.08), (298.52, 352.34)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_359.json'), ((211.35, 426.63), (450.68, 347.96)),((221.35, 436.63), (460.68, 357.96)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_119.json'), ((451.05, 608.61), (514.1, 700.76)),((461.05, 618.61), (524.1, 710.76)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_375.json'), ((262.62, 443.68), (514.1, 414.46)),((272.62, 453.68), (524.1, 424.46)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_230.json'), ((707.0, 448.0), (901.0, 1419.0)),((717.0, 458.0), (911.0, 1429.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_48.json'), ((418.5, 610.5), (462.0, 354.0)),((428.5, 620.5), (472.0, 364.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_158.json'), ((227.8, 403.53), (317.23, 410.43)),((237.8, 413.53), (327.23, 420.43)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_334.json'), ((537.47, 756.23), (267.65, 226.87)),((547.47, 766.23), (277.65, 236.87)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_621.json'), ((581.62, 1135.52), (460.57, 627.46)),((591.62, 1145.52), (470.57, 637.46)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_3.json'), ((275.5, 667.5), (736.0, 556.0)),((285.5, 677.5), (746.0, 566.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_271.json'), ((513.57, 407.52), (627.51, 866.58)),((523.57, 417.52), (637.51, 876.58)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_503.json'), ((175.99, 374.84), (219.98, 185.36)),((185.99, 384.84), (229.98, 195.36)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_153.json'), ((351.98, 594.32), (378.39, 307.44)),((361.98, 604.32), (388.39, 317.44)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_446.json'), ((409.29, 538.21), (502.36, 675.08)),((419.29, 548.21), (512.36, 685.08)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_14.json'), ((1001.32, 343.75), (377.2, 270.31)),((1011.32, 353.75), (387.2, 280.31)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_295.json'), ((478.2, 1333.12), (373.85, 545.01)),((488.2, 1343.12), (383.85, 555.01)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_8.json'), ((543.68, 430.56), (404.29, 329.02)),((553.68, 440.56), (414.29, 339.02)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_554.json'), ((266.0, 292.0), (167.0, 221.0)),((276.0, 302.0), (177.0, 231.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_43.json'), ((407.75, 478.12), (227.23, 269.71)),((417.75, 488.12), (237.23, 279.71)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_112.json'), ((446.13, 556.48), (300.14, 343.03)),((456.13, 566.48), (310.14, 353.03)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_407.json'), ((286.3, 671.05), (193.45, 239.44)),((296.3, 681.05), (203.45, 249.44)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_391.json'), ((376.38, 835.17), (443.13, 300.96)),((386.38, 845.17), (453.13, 310.96)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_145.json'), ((457.5, 549.5), (464.0, 632.0)),((467.5, 559.5), (474.0, 642.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_79.json'), ((532.99, 515.46), (387.8, 506.19)),((542.99, 525.46), (397.8, 516.19)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_352.json'), ((308.64, 640.77), (440.29, 625.03)),((318.64, 650.77), (450.29, 635.03)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_186.json'), ((448.7, 508.26), (496.46, 663.63)),((458.7, 518.26), (506.46, 673.63)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_169.json'), ((454.55, 611.28), (307.07, 267.13)),((464.55, 621.28), (317.07, 277.13)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_240.json'), ((679.55, 596.65), (212.35, 284.09)),((689.55, 606.65), (222.35, 294.09)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_610.json'), ((487.37, 1955.36), (237.88, 326.5)),((497.37, 1965.36), (247.88, 336.5)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_256.json'), ((784.0, 588.48), (711.61, 1018.33)),((794.0, 598.48), (721.61, 1028.33)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_38.json'), ((493.02, 574.44), (291.14, 366.23)),((503.02, 584.44), (301.14, 376.23)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_201.json'), ((475.14, 655.94), (554.18, 870.45)),((485.14, 665.94), (564.18, 880.45)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_333.json'), ((486.77, 715.98), (492.37, 391.22)),((496.77, 725.98), (502.37, 401.22)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_18.json'), ((550.79, 505.11), (271.54, 376.65)),((560.79, 515.11), (281.54, 386.65)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_276.json'), ((573.59, 800.06), (370.66, 537.94)),((583.59, 810.06), (380.66, 547.94)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_221.json'), ((539.31, 508.49), (357.68, 500.59)),((549.31, 518.49), (367.68, 510.59)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_108.json'), ((307.0, 495.0), (499.0, 541.0)),((317.0, 505.0), (509.0, 551.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_372.json'), ((555.5, 833.0), (695.0, 504.0)),((565.5, 843.0), (705.0, 514.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_237.json'), ((413.55, 784.67), (464.72, 763.18)),((423.55, 794.67), (474.72, 773.18)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_325.json'), ((273.61, 696.35), (349.55, 395.47)),((283.61, 706.35), (359.55, 405.47)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_260.json'), ((516.67, 730.49), (545.87, 380.07)),((526.67, 740.49), (555.87, 390.07)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_519.json'), ((522.83, 645.98), (891.98, 736.21)),((532.83, 655.98), (901.98, 746.21)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_75.json'), ((371.14, 504.62), (491.23, 427.31)),((381.14, 514.62), (501.23, 437.31)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_427.json'), ((278.0, 588.5), (598.0, 451.0)),((288.0, 598.5), (608.0, 461.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_562.json'), ((409.0, 527.0), (319.0, 267.0)),((419.0, 537.0), (329.0, 277.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_132.json'), ((485.59, 528.72), (766.35, 869.23)),((495.59, 538.72), (776.35, 879.23)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_165.json'), ((427.61, 525.43), (564.71, 486.63)),((437.61, 535.43), (574.71, 496.63)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_34.json'), ((492.0, 263.5), (203.0, 240.0)),((502.0, 273.5), (213.0, 250.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_466.json'), ((720.69, 547.67), (437.19, 143.01)),((730.69, 557.67), (447.19, 153.01)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_523.json'), ((195.35, 63.23), (50.19, 16.63)),((205.35, 73.23), (60.19, 26.63)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_173.json'), ((432.13, 504.41), (818.79, 628.11)),((442.13, 514.41), (828.79, 638.11)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_63.json'), ((548.0, 391.0), (374.05, 301.3)),((558.0, 401.0), (384.05, 311.3)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_431.json'), ((366.07, 440.2), (290.24, 236.41)),((376.07, 450.2), (300.24, 246.41)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_124.json'), ((521.04, 547.93), (439.95, 561.34)),((531.04, 557.93), (449.95, 571.34)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_574.json'), ((342.76, 628.01), (643.98, 469.41)),((352.76, 638.01), (653.98, 479.41)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_430.json'), ((498.23, 523.64), (425.36, 493.01)),((508.23, 533.64), (435.36, 503.01)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_575.json'), ((675.87, 495.22), (356.11, 294.84)),((685.87, 505.22), (366.11, 304.84)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_62.json'), ((506.85, 505.98), (257.07, 320.44)),((516.85, 515.98), (267.07, 330.44)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_522.json'), ((364.5, 539.0), (545.0, 602.0)),((374.5, 549.0), (555.0, 612.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_35.json'), ((330.5, 605.5), (632.0, 502.0)),((340.5, 615.5), (642.0, 512.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_471.json'), ((401.26, 542.67), (454.68, 537.35)),((411.26, 552.67), (464.68, 547.35)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_164.json'), ((785.5, 1170.5), (42.0, 212.0)),((795.5, 1180.5), (52.0, 222.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_534.json'), ((298.5, 672.5), (590.0, 458.0)),((308.5, 682.5), (600.0, 468.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_23.json'), ((293.16, 489.17), (331.02, 403.45)),((303.16, 499.17), (341.02, 413.45)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_426.json'), ((333.02, 553.65), (406.2, 539.02)),((343.02, 563.65), (416.2, 549.02)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_563.json'), ((305.5, 525.0), (451.0, 396.0)),((315.5, 535.0), (461.0, 406.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_133.json'), ((438.5, 511.0), (489.0, 406.0)),((448.5, 521.0), (499.0, 416.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_74.json'), ((351.16, 336.39), (491.11, 601.05)),((361.16, 346.39), (501.11, 611.05)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_518.json'), ((429.26, 422.22), (376.82, 301.94)),((439.26, 432.22), (386.82, 311.94)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_148.json'), ((310.63, 271.82), (220.49, 275.4)),((320.63, 281.82), (230.49, 285.4)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_324.json'), ((400.42, 765.43), (248.33, 265.52)),((410.42, 775.43), (258.33, 275.52)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_261.json'), ((545.02, 834.97), (451.37, 305.62)),((555.02, 844.97), (461.37, 315.62)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_58.json'), ((470.0, 591.5), (430.0, 357.0)),((480.0, 601.5), (440.0, 367.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_373.json'), ((281.06, 445.71), (455.99, 388.4)),((291.06, 455.71), (465.99, 398.4)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_109.json'), ((294.62, 474.82), (578.44, 446.41)),((304.62, 484.82), (588.44, 456.41)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_220.json'), ((312.46, 637.51), (327.38, 490.13)),((322.46, 647.51), (337.38, 500.13)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_298.json'), ((701.0, 1319.5), (1325.0, 1744.0)),((711.0, 1329.5), (1335.0, 1754.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_19.json'), ((512.93, 588.65), (605.44, 474.49)),((522.93, 598.65), (615.44, 484.49)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_5.json'), ((437.56, 630.26), (275.37, 197.99)),((447.56, 640.26), (285.37, 207.99)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_277.json'), ((399.42, 242.88), (334.07, 237.01)),((409.42, 252.88), (344.07, 247.01)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_81.json'), ((471.28, 584.58), (446.31, 608.03)),((481.28, 594.58), (456.31, 618.03)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_596.json'), ((934.66, 809.3), (504.65, 678.01)),((944.66, 819.3), (514.65, 688.01)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_607.json'), ((687.33, 1169.61), (440.28, 541.77)),((697.33, 1179.61), (450.28, 551.77)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_257.json'), ((253.41, 651.21), (251.28, 367.35)),((263.41, 661.21), (261.28, 377.35)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_39.json'), ((353.5, 518.0), (597.0, 444.0)),((363.5, 528.0), (607.0, 454.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_191.json'), ((498.0, 642.5), (518.0, 753.0)),((508.0, 652.5), (528.0, 763.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_241.json'), ((683.37, 478.7), (250.57, 326.1)),((693.37, 488.7), (260.57, 336.1)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_187.json'), ((542.5, 620.0), (796.0, 565.0)),((552.5, 630.0), (806.0, 575.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_538.json'), ((401.61, 527.16), (451.14, 563.94)),((411.61, 537.16), (461.14, 573.94)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_492.json'), ((395.19, 689.96), (187.98, 149.82)),((405.19, 699.96), (197.98, 159.82)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_97.json'), ((458.61, 591.02), (408.78, 487.06)),((468.61, 601.02), (418.78, 497.06)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_328.json'), ((475.97, 962.74), (585.72, 428.72)),((485.97, 972.74), (595.72, 438.72)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_144.json'), ((406.88, 390.63), (327.88, 261.04)),((416.88, 400.63), (337.88, 271.04)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_514.json'), ((366.31, 413.03), (285.05, 350.09)),((376.31, 423.03), (295.05, 360.09)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_390.json'), ((365.31, 1007.98), (512.14, 670.28)),((375.31, 1017.98), (522.14, 680.28)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_369.json'), ((361.53, 722.0), (421.06, 287.94)),((371.53, 732.0), (431.06, 297.94)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_386.json'), ((473.0, 397.0), (239.0, 165.0)),((483.0, 407.0), (249.0, 175.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_105.json'), ((457.9, 523.11), (560.54, 678.88)),((467.9, 533.11), (570.54, 688.88)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_555.json'), ((363.08, 506.98), (458.63, 377.42)),((373.08, 516.98), (468.63, 387.42)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_15.json'), ((352.3, 372.07), (448.13, 391.11)),((362.3, 382.07), (458.13, 401.11)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_9.json'), ((332.31, 767.82), (448.39, 400.25)),((342.31, 777.82), (458.39, 410.25)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_152.json'), ((436.5, 548.5), (514.0, 414.0)),((446.5, 558.5), (524.0, 424.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_447.json'), ((404.03, 403.61), (204.58, 254.74)),((414.03, 413.61), (214.58, 264.74)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_203.json'), ((651.16, 296.03), (248.3, 352.12)),((661.16, 306.03), (258.3, 362.12)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_82.json'), ((436.5, 463.0), (293.0, 242.0)),((446.5, 473.0), (303.0, 252.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_595.json'), ((754.0, 1280.48), (776.24, 920.92)),((764.0, 1290.48), (786.24, 930.92)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_604.json'), ((498.76, 1190.61), (1027.97, 785.0)),((508.76, 1200.61), (1037.97, 795.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_254.json'), ((408.33, 997.62), (233.75, 332.61)),((418.33, 1007.62), (243.75, 342.61)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_468.json'), ((417.24, 201.79), (205.09, 261.16)),((427.24, 211.79), (215.09, 271.16)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_242.json'), ((567.5, 749.66), (454.9, 481.07)),((577.5, 759.66), (464.9, 491.07)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_491.json'), ((444.0, 498.34), (481.17, 644.84)),((454.0, 508.34), (491.17, 654.84)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_184.json'), ((511.28, 543.24), (312.48, 419.15)),((521.28, 553.24), (322.48, 429.15)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_350.json'), ((331.64, 916.45), (696.88, 535.14)),((341.64, 926.45), (706.88, 545.14)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_94.json'), ((470.0, 783.32), (280.18, 320.53)),((480.0, 793.32), (290.18, 330.53)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_429.json'), ((420.23, 616.84), (664.43, 546.44)),((430.23, 626.84), (674.43, 556.44)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_452.json'), ((731.53, 561.49), (573.89, 317.21)),((741.53, 571.49), (583.89, 327.21)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_393.json'), ((512.37, 1055.28), (472.62, 292.38)),((522.37, 1065.28), (482.62, 302.38)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_57.json'), ((339.6, 270.94), (109.21, 145.89)),((349.6, 280.94), (119.21, 155.89)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_110.json'), ((495.78, 637.62), (535.14, 678.9)),((505.78, 647.62), (545.14, 688.9)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_385.json'), ((330.81, 917.53), (696.87, 536.98)),((340.81, 927.53), (706.87, 546.98)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_106.json'), ((471.2, 608.4), (441.51, 644.53)),((481.2, 618.4), (451.51, 654.53)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_556.json'), ((525.57, 578.26), (432.97, 498.43)),((535.57, 588.26), (442.97, 508.43)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_278.json'), ((629.5, 517.5), (288.0, 476.0)),((639.5, 527.5), (298.0, 486.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_16.json'), ((385.71, 430.33), (409.03, 469.57)),((395.71, 440.33), (419.03, 479.57)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_126.json'), ((307.0, 495.0), (499.0, 541.0)),((317.0, 505.0), (509.0, 551.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_576.json'), ((477.0, 433.5), (388.0, 475.0)),((487.0, 443.5), (398.0, 485.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_433.json'), ((434.02, 253.81), (183.76, 173.62)),((444.02, 263.81), (193.76, 183.62)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_171.json'), ((434.09, 253.75), (183.75, 173.59)),((444.09, 263.75), (193.75, 183.59)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_608.json'), ((520.46, 1090.73), (398.27, 613.23)),((530.46, 1100.73), (408.27, 623.23)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_472.json'), ((276.96, 472.21), (400.28, 341.64)),((286.96, 482.21), (410.28, 351.64)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_560.json'), ((830.27, 389.54), (219.93, 255.77)),((840.27, 399.54), (229.93, 265.77)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_130.json'), ((438.31, 532.38), (627.3, 823.13)),((448.31, 542.38), (637.3, 833.13)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_219.json'), ((295.38, 648.18), (418.68, 591.45)),((305.38, 658.18), (428.68, 601.45)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_98.json'), ((491.56, 442.76), (321.95, 382.08)),((501.56, 452.76), (331.95, 392.08)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_235.json'), ((495.02, 998.13), (604.22, 409.09)),((505.02, 1008.13), (614.22, 419.09)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_370.json'), ((331.6, 652.32), (465.12, 570.73)),((341.6, 662.32), (475.12, 580.73)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_389.json'), ((512.0, 1126.5), (454.0, 315.0)),((522.0, 1136.5), (464.0, 325.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_6.json'), ((480.06, 544.83), (463.77, 380.43)),((490.06, 554.83), (473.77, 390.43)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_275.json'), ((484.15, 596.79), (599.23, 364.77)),((494.15, 606.79), (609.23, 374.77)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_449.json'), ((223.5, 553.5), (400.0, 304.0)),((233.5, 563.5), (410.0, 314.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_222.json'), ((492.31, 807.48), (598.08, 430.57)),((502.31, 817.48), (608.08, 440.57)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_234.json'), ((399.72, 634.65), (388.6, 253.01)),((409.72, 644.65), (398.6, 263.01)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_371.json'), ((414.0, 687.5), (603.0, 710.0)),((424.0, 697.5), (613.0, 720.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_263.json'), ((274.33, 614.31), (321.21, 496.28)),((284.33, 624.31), (331.21, 506.28)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_561.json'), ((374.09, 491.35), (352.34, 401.02)),((384.09, 501.35), (362.34, 411.02)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_131.json'), ((308.78, 352.64), (401.18, 359.21)),((318.78, 362.64), (411.18, 369.21)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_424.json'), ((426.5, 434.0), (553.0, 448.0)),((436.5, 444.0), (563.0, 458.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_21.json'), ((349.97, 533.47), (390.48, 326.52)),((359.97, 543.47), (400.48, 336.52)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_166.json'), ((289.76, 616.01), (396.15, 468.77)),((299.76, 626.01), (406.15, 478.77)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_536.json'), ((405.86, 500.76), (679.09, 557.98)),((415.86, 510.76), (689.09, 567.98)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_37.json'), ((438.27, 517.37), (559.56, 632.07)),((448.27, 527.37), (569.56, 642.07)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_259.json'), ((442.97, 909.79), (447.74, 292.46)),((452.97, 919.79), (457.74, 302.46)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_609.json'), ((741.76, 1300.08), (281.37, 395.65)),((751.76, 1310.08), (291.37, 405.65)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_520.json'), ((466.56, 236.39), (134.85, 313.52)),((476.56, 246.39), (144.85, 323.52)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_127.json'), ((444.06, 980.42), (283.78, 360.15)),((454.06, 990.42), (293.78, 370.15)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_577.json'), ((545.82, 1141.28), (845.28, 952.9)),((555.82, 1151.28), (855.28, 962.9)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_598.json'), ((635.19, 1706.09), (798.03, 629.97)),((645.19, 1716.09), (808.03, 639.97)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_432.json'), ((305.49, 131.77), (84.23, 114.84)),((315.49, 141.77), (94.23, 124.84)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_445.json'), ((439.74, 463.53), (313.05, 367.27)),((449.74, 473.53), (323.05, 377.27)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_150.json'), ((418.5, 610.5), (462.0, 354.0)),((428.5, 620.5), (472.0, 364.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_17.json'), ((216.18, 638.04), (427.52, 534.63)),((226.18, 648.04), (437.52, 544.63)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_107.json'), ((398.64, 327.52), (363.52, 388.54)),((408.64, 337.52), (373.52, 398.54)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_557.json'), ((337.28, 373.07), (440.84, 508.22)),((347.28, 383.07), (450.84, 518.22)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_40.json'), ((437.98, 481.08), (484.69, 593.64)),((447.98, 491.08), (494.69, 603.64)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_404.json'), ((545.0, 827.5), (302.0, 219.0)),((555.0, 837.5), (312.0, 229.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_238.json'), ((465.47, 782.68), (599.18, 840.55)),((475.47, 792.68), (609.18, 850.55)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_392.json'), ((716.27, 966.67), (278.39, 401.62)),((726.27, 976.67), (288.39, 411.62)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_56.json'), ((447.61, 597.28), (409.02, 469.49)),((457.61, 607.28), (419.02, 479.49)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_453.json'), ((488.5, 700.5), (438.0, 330.0)),((498.5, 710.5), (448.0, 340.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_280.json'), ((744.65, 906.31), (1060.3, 1615.34)),((754.65, 916.31), (1070.3, 1625.34)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_428.json'), ((393.29, 500.24), (495.08, 608.98)),((403.29, 510.24), (505.08, 618.98)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_351.json'), ((299.13, 313.57), (249.66, 181.43)),((309.13, 323.57), (259.66, 191.43)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_95.json'), ((389.15, 220.62), (181.64, 137.12)),((399.15, 230.62), (191.64, 147.12)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_214.json'), ((841.36, 845.67), (253.93, 375.24)),((851.36, 855.67), (263.93, 385.24)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_193.json'), ((928.79, 382.36), (369.2, 255.63)),((938.79, 392.36), (379.2, 265.63)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_605.json'), ((708.22, 835.38), (638.23, 701.65)),((718.22, 845.38), (648.23, 711.65)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_202.json'), ((471.62, 708.97), (285.99, 227.7)),((481.62, 718.97), (295.99, 237.7)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_120.json'), ((348.1, 340.82), (417.52, 397.17)),((358.1, 350.82), (427.52, 407.17)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_67.json'), ((325.85, 592.19), (450.05, 411.39)),((335.85, 602.19), (460.05, 421.39)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_88.json'), ((291.5, 335.5), (432.0, 348.0)),((301.5, 345.5), (442.0, 358.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_30.json'), ((432.5, 624.5), (704.0, 594.0)),((442.5, 634.5), (714.0, 604.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_161.json'), ((803.13, 170.59), (246.25, 332.56)),((813.13, 180.59), (256.25, 342.56)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_26.json'), ((451.25, 386.67), (243.52, 323.02)),((461.25, 396.67), (253.52, 333.02)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_618.json'), ((517.0, 1162.5), (528.0, 407.0)),((527.0, 1172.5), (538.0, 417.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_566.json'), ((298.32, 672.11), (592.79, 459.93)),((308.32, 682.11), (602.79, 469.93)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_136.json'), ((897.3, 354.94), (410.2, 309.97)),((907.3, 364.94), (420.2, 319.97)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_423.json'), ((330.5, 431.5), (688.0, 534.0)),((340.5, 441.5), (698.0, 544.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_589.json'), ((376.39, 1072.53), (587.42, 528.9)),((386.39, 1082.53), (597.42, 538.9)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_71.json'), ((446.71, 618.07), (457.17, 560.1)),((456.71, 628.07), (467.17, 570.1)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_458.json'), ((324.98, 148.79), (50.52, 49.22)),((334.98, 158.79), (60.52, 59.22)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_264.json'), ((260.14, 584.54), (336.49, 516.17)),((270.14, 594.54), (346.49, 526.17)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_399.json'), ((516.9, 920.52), (758.65, 524.18)),((526.9, 930.52), (768.65, 534.18)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_233.json'), ((549.03, 623.58), (804.87, 570.88)),((559.03, 633.58), (814.87, 580.88)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_419.json'), ((300.0, 542.5), (602.0, 465.0)),((310.0, 552.5), (612.0, 475.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_272.json'), ((513.96, 946.95), (855.15, 599.77)),((523.96, 956.95), (865.15, 609.77)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_337.json'), ((479.98, 262.29), (205.21, 300.8)),((489.98, 272.29), (215.21, 310.8)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_205.json'), ((379.12, 819.12), (644.22, 811.04)),((389.12, 829.12), (654.22, 821.04)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_84.json'), ((324.5, 432.5), (326.0, 314.0)),((334.5, 442.5), (336.0, 324.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_439.json'), ((475.96, 537.63), (597.16, 488.99)),((485.96, 547.63), (607.16, 498.99)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_593.json'), ((558.24, 1278.56), (566.72, 514.33)),((568.24, 1288.56), (576.72, 524.33)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_252.json'), ((317.55, 728.04), (256.11, 413.25)),((327.55, 738.04), (266.11, 423.25)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_194.json'), ((455.52, 707.23), (485.42, 669.25)),((465.52, 717.23), (495.42, 679.25)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_244.json'), ((380.46, 575.51), (415.17, 645.28)),((390.46, 585.51), (425.17, 655.28)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_497.json'), ((583.6, 351.77), (239.94, 317.75)),((593.6, 361.77), (249.94, 327.75)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_92.json'), ((444.5, 691.5), (894.0, 1000.0)),((454.5, 701.5), (904.0, 1010.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_213.json'), ((490.19, 766.22), (688.17, 984.44)),((500.19, 776.22), (698.17, 994.44)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_585.json'), ((734.27, 899.87), (475.76, 731.03)),((744.27, 909.87), (485.76, 741.03)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_268.json'), ((532.34, 444.03), (446.97, 715.88)),((542.34, 454.03), (456.97, 725.88)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_454.json'), ((609.99, 617.96), (367.58, 414.84)),((619.99, 627.96), (377.58, 424.84)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_395.json'), ((646.81, 691.31), (160.98, 242.31)),((656.81, 701.31), (170.98, 252.31)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_51.json'), ((424.5, 365.0), (369.0, 302.0)),((434.5, 375.0), (379.0, 312.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_546.json'), ((133.58, 121.15), (44.86, 26.1)),((143.58, 131.15), (54.86, 36.1)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_116.json'), ((237.84, 584.92), (268.91, 339.41)),((247.84, 594.92), (278.91, 349.41)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_383.json'), ((554.79, 1032.45), (447.72, 540.29)),((564.79, 1042.45), (457.72, 550.29)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_229.json'), ((545.71, 773.34), (332.59, 472.36)),((555.71, 783.34), (342.59, 482.36)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_47.json'), ((248.5, 669.0), (617.0, 502.0)),((258.5, 679.0), (627.0, 512.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_100.json'), ((410.28, 531.44), (450.48, 561.54)),((420.28, 541.44), (460.48, 571.54)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_10.json'), ((426.34, 527.78), (443.69, 552.28)),((436.34, 537.78), (453.69, 562.28)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_291.json'), ((503.62, 1070.42), (574.73, 395.54)),((513.62, 1080.42), (584.73, 405.54)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_507.json'), ((455.5, 524.0), (839.0, 632.0)),((465.5, 534.0), (849.0, 642.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_157.json'), ((439.22, 606.84), (607.75, 489.76)),((449.22, 616.84), (617.75, 499.76)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_506.json'), ((299.21, 567.95), (346.05, 412.17)),((309.21, 577.95), (356.05, 422.17)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_156.json'), ((777.53, 392.67), (199.91, 237.9)),((787.53, 402.67), (209.91, 247.9)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_11.json'), ((306.12, 514.95), (361.16, 409.19)),((316.12, 524.95), (371.16, 419.19)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_551.json'), ((429.98, 578.7), (570.4, 646.4)),((439.98, 588.7), (580.4, 656.4)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_382.json'), ((604.9, 837.07), (267.03, 404.23)),((614.9, 847.07), (277.03, 414.23)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_402.json'), ((402.77, 839.19), (509.26, 295.79)),((412.77, 849.19), (519.26, 305.79)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_547.json'), ((264.5, 489.0), (523.0, 422.0)),((274.5, 499.0), (533.0, 432.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_117.json'), ((232.87, 450.57), (216.92, 257.82)),((242.87, 460.57), (226.92, 267.82)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_455.json'), ((391.3, 511.9), (440.88, 310.6)),((401.3, 521.9), (450.88, 320.6)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_140.json'), ((393.5, 502.0), (493.0, 468.0)),((403.5, 512.0), (503.0, 478.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_357.json'), ((304.14, 505.88), (544.49, 399.32)),((314.14, 515.88), (554.49, 409.32)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_93.json'), ((395.21, 549.76), (536.12, 686.86)),((405.21, 559.76), (546.12, 696.86)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_496.json'), ((386.93, 508.41), (355.1, 382.68)),((396.93, 518.41), (365.1, 392.68)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_245.json'), ((435.39, 836.56), (309.25, 485.71)),((445.39, 846.56), (319.25, 495.71)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_615.json'), ((554.0, 1120.0), (503.0, 709.0)),((564.0, 1130.0), (513.0, 719.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_603.json'), ((545.6, 1209.75), (1080.14, 886.61)),((555.6, 1219.75), (1090.14, 896.61)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_592.json'), ((394.91, 1091.11), (587.5, 523.82)),((404.91, 1101.11), (597.5, 533.82)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_273.json'), ((280.0, 665.5), (310.0, 463.0)),((290.0, 675.5), (320.0, 473.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_1.json'), ((457.0, 467.5), (632.0, 507.0)),((467.0, 477.5), (642.0, 517.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_418.json'), ((464.2, 840.0), (516.92, 671.27)),((474.2, 850.0), (526.92, 681.27)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_398.json'), ((848.85, 1698.6), (261.14, 152.84)),((858.85, 1708.6), (271.14, 162.84)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_232.json'), ((494.88, 793.51), (939.01, 685.44)),((504.88, 803.51), (949.01, 695.44)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_377.json'), ((610.79, 707.44), (201.54, 141.64)),((620.79, 717.44), (211.54, 151.64)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_265.json'), ((330.71, 825.98), (191.24, 287.24)),((340.71, 835.98), (201.24, 297.24)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_459.json'), ((378.2, 479.64), (377.01, 427.75)),((388.2, 489.64), (387.01, 437.75)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_70.json'), ((247.37, 216.64), (175.73, 219.47)),((257.37, 226.64), (185.73, 229.47)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_137.json'), ((700.69, 578.22), (324.32, 344.06)),((710.69, 588.22), (334.32, 354.06)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_422.json'), ((236.87, 527.7), (317.29, 285.21)),((246.87, 537.7), (327.29, 295.21)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_588.json'), ((347.36, 1044.09), (568.78, 536.26)),((357.36, 1054.09), (578.78, 546.26)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_27.json'), ((415.43, 539.54), (343.12, 389.96)),((425.43, 549.54), (353.12, 399.96)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_619.json'), ((620.31, 1028.16), (561.48, 413.41)),((630.31, 1038.16), (571.48, 423.41)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_249.json'), ((526.04, 604.38), (504.64, 684.86)),((536.04, 614.38), (514.64, 694.86)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_160.json'), ((468.4, 516.41), (366.09, 295.0)),((478.4, 526.41), (376.09, 305.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_530.json'), ((500.28, 583.51), (483.78, 359.9)),((510.28, 593.51), (493.78, 369.9)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_31.json'), ((477.0, 551.0), (411.0, 477.0)),((487.0, 561.0), (421.0, 487.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_176.json'), ((290.5, 407.47), (141.01, 130.57)),((300.5, 417.47), (151.01, 140.57)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_89.json'), ((275.5, 577.5), (408.0, 340.0)),((285.5, 587.5), (418.0, 350.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_571.json'), ((477.97, 535.32), (411.21, 446.37)),((487.97, 545.32), (421.21, 456.37)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_pressure_434.json'), ((457.38, 616.27), (428.81, 569.46)),((467.38, 626.27), (438.81, 579.46)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_293.json'), ((778.28, 1299.12), (561.75, 639.02)),((788.28, 1309.12), (571.75, 649.02)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_339.json'), ((473.2, 625.01), (389.51, 460.75)),((483.2, 635.01), (399.51, 470.75)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_6.json'), ((527.48, 443.58), (391.2, 326.96)),((537.48, 453.58), (401.2, 336.96)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_102.json'), ((340.59, 372.71), (364.9, 294.24)),((350.59, 382.71), (374.9, 304.24)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_397.json'), ((364.01, 205.0), (260.98, 281.05)),((374.01, 215.0), (270.98, 291.05)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_378.json'), ((159.45, 57.43), (36.44, 53.67)),((169.45, 67.43), (46.44, 63.67)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_303.json'), ((445.75, 955.97), (394.63, 465.95)),((455.75, 965.97), (404.63, 475.95)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_315.json'), ((578.66, 569.71), (528.81, 659.16)),((588.66, 579.71), (538.81, 669.16)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_342.json'), ((469.99, 852.23), (266.84, 312.26)),((479.99, 862.23), (276.84, 322.26)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_70.json'), ((433.5, 667.5), (872.0, 1048.0)),((443.5, 677.5), (882.0, 1058.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_159.json'), ((540.5, 173.5), (144.0, 202.0)),((550.5, 183.5), (154.0, 212.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_289.json'), ((687.66, 581.25), (729.32, 666.39)),((697.66, 591.25), (739.32, 676.39)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_319.json'), ((500.16, 447.28), (632.85, 674.77)),((510.16, 457.28), (642.85, 684.77)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_318.json'), ((574.12, 738.15), (458.24, 382.34)),((584.12, 748.15), (468.24, 392.34)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_288.json'), ((972.0, 583.5), (700.0, 615.0)),((982.0, 593.5), (710.0, 625.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_322.json'), ((482.26, 985.9), (287.43, 314.07)),((492.26, 995.9), (297.43, 324.07)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_375.json'), ((61.81, 121.94), (69.9, 46.41)),((71.81, 131.94), (79.9, 56.41)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_271.json'), ((540.48, 829.1), (532.15, 451.53)),((550.48, 839.1), (542.15, 461.53)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_334.json'), ((584.9, 1016.64), (544.09, 480.67)),((594.9, 1026.64), (554.09, 490.67)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_343.json'), ((414.68, 424.7), (83.14, 96.61)),((424.68, 434.7), (93.14, 106.61)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_314.json'), ((468.0, 642.0), (633.0, 539.0)),((478.0, 652.0), (643.0, 549.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_30.json'), ((429.94, 390.53), (377.63, 453.92)),((439.94, 400.53), (387.63, 463.92)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_302.json'), ((374.26, 1303.48), (647.5, 554.38)),((384.26, 1313.48), (657.5, 564.38)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_67.json'), ((527.48, 443.58), (391.2, 326.96)),((537.48, 453.58), (401.2, 336.96)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_292.json'), ((386.8, 841.77), (531.09, 475.09)),((396.8, 851.77), (541.09, 485.09)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_338.json'), ((882.59, 1129.99), (489.64, 403.35)),((892.59, 1139.99), (499.64, 413.35)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_276.json'), ((531.1, 352.81), (462.11, 495.04)),((541.1, 362.81), (472.11, 505.04)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_333.json'), ((572.91, 660.43), (420.23, 481.67)),((582.91, 670.43), (430.23, 491.67)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_299.json'), ((360.29, 784.4), (634.81, 539.75)),((370.29, 794.4), (644.81, 549.75)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_149.json'), ((430.42, 678.5), (251.63, 179.13)),((440.42, 688.5), (261.63, 189.13)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_132.json'), ((716.19, 601.5), (532.54, 355.05)),((726.19, 611.5), (542.54, 365.05)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_309.json'), ((482.0, 474.5), (539.0, 636.0)),((492.0, 484.5), (549.0, 646.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_348.json'), ((386.0, 230.0), (277.0, 243.0)),((396.0, 240.0), (287.0, 253.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_295.json'), ((709.96, 815.02), (842.34, 721.55)),((719.96, 825.02), (852.34, 731.55)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_391.json'), ((182.95, 315.78), (332.23, 397.75)),((192.95, 325.78), (342.23, 407.75)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_329.json'), ((420.67, 701.17), (439.23, 390.48)),((430.67, 711.17), (449.23, 400.48)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_283.json'), ((315.09, 421.99), (140.4, 155.97)),((325.09, 431.99), (150.4, 165.97)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_217.json'), ((599.94, 1484.17), (682.99, 916.33)),((609.94, 1494.17), (692.99, 926.33)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_313.json'), ((407.08, 863.73), (789.32, 685.74)),((417.08, 873.73), (799.32, 695.74)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_344.json'), ((637.5, 844.0), (614.0, 717.0)),((647.5, 854.0), (624.0, 727.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_128.json'), ((551.08, 597.59), (465.22, 658.21)),((561.08, 607.59), (475.22, 668.21)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_98.json'), ((44.06, 154.09), (47.14, 42.66)),((54.06, 164.09), (57.14, 52.66)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_129.json'), ((579.62, 574.32), (513.53, 739.67)),((589.62, 584.32), (523.53, 749.67)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_345.json'), ((742.5, 789.5), (778.0, 686.0)),((752.5, 799.5), (788.0, 696.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_312.json'), ((315.35, 368.13), (367.32, 325.2)),((325.35, 378.13), (377.32, 335.2)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_353.json'), ((86.0, 65.0), (101.0, 93.0)),((96.0, 75.0), (111.0, 103.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_144.json'), ((782.26, 681.38), (565.58, 740.73)),((792.26, 691.38), (575.58, 750.73)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_328.json'), ((740.13, 1340.17), (421.39, 489.92)),((750.13, 1350.17), (431.39, 499.92)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_294.json'), ((657.45, 1165.26), (630.22, 532.71)),((667.45, 1175.26), (640.22, 542.71)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_308.json'), ((439.54, 839.49), (579.28, 677.53)),((449.54, 849.49), (589.28, 687.53)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_324.json'), ((348.09, 396.96), (235.22, 203.66)),((358.09, 406.96), (245.22, 213.66)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_41.json'), ((527.48, 443.58), (391.2, 326.96)),((537.48, 453.58), (401.2, 336.96)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_277.json'), ((475.86, 468.8), (935.05, 793.14)),((485.86, 478.8), (945.05, 803.14)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_332.json'), ((500.67, 677.28), (636.26, 555.36)),((510.67, 687.28), (646.26, 565.36)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_298.json'), ((288.19, 157.22), (245.44, 272.56)),((298.19, 167.22), (255.44, 282.56)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_78.json'), ((77.87, 81.49), (91.69, 30.0)),((87.87, 91.49), (101.69, 40.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_97.json'), ((416.0, 748.5), (837.0, 886.0)),((426.0, 758.5), (847.0, 896.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_39.json'), ((332.73, 244.79), (227.5, 181.0)),((342.73, 254.79), (237.5, 191.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_130.json'), ((549.15, 629.38), (460.13, 666.14)),((559.15, 639.38), (470.13, 676.14)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_327.json'), ((634.56, 913.24), (505.21, 597.2)),((644.56, 923.24), (515.21, 607.2)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_15.json'), ((327.39, 591.93), (246.15, 175.56)),((337.39, 601.93), (256.15, 185.56)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_235.json'), ((620.33, 1147.17), (994.24, 509.65)),((630.33, 1157.17), (1004.24, 519.65)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_331.json'), ((561.07, 587.9), (546.99, 490.86)),((571.07, 597.9), (556.99, 500.86)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_274.json'), ((452.77, 535.52), (377.41, 449.86)),((462.77, 545.52), (387.41, 459.86)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_346.json'), ((55.0, 90.5), (58.0, 51.0)),((65.0, 100.5), (68.0, 61.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_311.json'), ((521.5, 134.5), (174.0, 638.0)),((531.5, 144.5), (184.0, 648.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_35.json'), ((156.31, 338.77), (110.31, 94.12)),((166.31, 348.77), (120.31, 104.12)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_307.json'), ((689.86, 860.28), (428.74, 355.7)),((699.86, 870.28), (438.74, 365.7)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_147.json'), ((360.5, 881.0), (211.0, 152.0)),((370.5, 891.0), (221.0, 162.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_281.json'), ((507.24, 806.15), (364.38, 323.76)),((517.24, 816.15), (374.38, 333.76)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_110.json'), ((465.09, 900.51), (239.63, 351.2)),((475.09, 910.51), (249.63, 361.2)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_151.json'), ((545.5, 910.0), (737.0, 514.0)),((555.5, 920.0), (747.0, 524.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_297.json'), ((400.93, 920.65), (445.07, 484.56)),((410.93, 930.65), (455.07, 494.56)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_296.json'), ((568.5, 634.0), (703.0, 632.0)),((578.5, 644.0), (713.0, 642.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_150.json'), ((490.5, 330.0), (94.8, 152.61)),((500.5, 340.0), (104.8, 162.61)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_59.json'), ((364.0, 174.0), (129.0, 101.0)),((374.0, 184.0), (139.0, 111.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_280.json'), ((360.64, 783.92), (634.33, 541.49)),((370.64, 793.92), (644.33, 551.49)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_146.json'), ((529.08, 833.2), (309.34, 221.26)),((539.08, 843.2), (319.34, 231.26)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_351.json'), ((239.37, 532.29), (203.78, 257.36)),((249.37, 542.29), (213.78, 267.36)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_243.json'), ((569.79, 718.34), (571.79, 854.9)),((579.79, 728.34), (581.79, 864.9)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_306.json'), ((514.27, 586.99), (499.48, 570.18)),((524.27, 596.99), (509.48, 580.18)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_34.json'), ((311.1, 334.57), (105.48, 84.7)),((321.1, 344.57), (115.48, 94.7)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_255.json'), ((457.22, 413.28), (540.64, 387.02)),((467.22, 423.28), (550.64, 397.02)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_347.json'), ((530.5, 1010.0), (789.0, 676.0)),((540.5, 1020.0), (799.0, 686.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_330.json'), ((516.37, 674.9), (790.06, 685.85)),((526.37, 684.9), (800.06, 695.85)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_14.json'), ((332.64, 244.62), (234.0, 185.09)),((342.64, 254.62), (244.0, 195.09)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_326.json'), ((446.0, 602.5), (530.0, 483.0)),((456.0, 612.5), (540.0, 493.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_131.json'), ((280.12, 659.92), (402.73, 284.08)),((290.12, 669.92), (412.73, 294.08)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_80.json'), ((457.5, 449.5), (496.0, 452.0)),((467.5, 459.5), (506.0, 462.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_340.json'), ((532.99, 854.16), (221.77, 270.31)),((542.99, 864.16), (231.77, 280.31)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_317.json'), ((436.0, 465.5), (934.0, 875.0)),((446.0, 475.5), (944.0, 885.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_301.json'), ((352.93, 810.2), (578.6, 740.63)),((362.93, 820.2), (588.6, 750.63)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_356.json'), ((339.52, 672.9), (186.23, 236.5)),((349.52, 682.9), (196.23, 246.5)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_4.json'), ((239.37, 532.29), (203.78, 257.36)),((249.37, 542.29), (213.78, 267.36)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_442.json'), ((267.0, 280.0), (191.0, 169.0)),((277.0, 290.0), (201.0, 179.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_291.json'), ((476.57, 1110.06), (644.42, 594.4)),((486.57, 1120.06), (654.42, 604.4)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_321.json'), ((760.68, 879.59), (1031.11, 800.59)),((770.68, 889.59), (1041.11, 810.59)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_376.json'), ((65.48, 39.75), (60.18, 59.87)),((75.48, 49.75), (70.18, 69.87)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_337.json'), ((455.75, 592.09), (485.14, 433.21)),((465.75, 602.09), (495.14, 443.21)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_272.json'), ((613.39, 1112.27), (350.2, 406.91)),((623.39, 1122.27), (360.2, 416.91)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_336.json'), ((823.07, 872.18), (544.13, 529.7)),((833.07, 882.18), (554.13, 539.7)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_9.json'), ((425.9, 451.43), (322.81, 363.58)),((435.9, 461.43), (332.81, 373.58)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_377.json'), ((150.0, 67.0), (55.0, 37.0)),((160.0, 77.0), (65.0, 47.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_232.json'), ((640.99, 521.39), (620.3, 425.66)),((650.99, 531.39), (630.3, 435.66)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_176.json'), ((1225.94, 684.83), (519.17, 744.97)),((1235.94, 694.83), (529.17, 754.97)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_290.json'), ((586.91, 865.99), (357.01, 395.87)),((596.91, 875.99), (367.01, 405.87)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_101.json'), ((443.85, 511.44), (304.54, 299.77)),((453.85, 521.44), (314.54, 309.77)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_5.json'), ((430.61, 587.28), (363.59, 292.22)),((440.61, 597.28), (373.59, 302.22)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_49.json'), ((400.0, 758.0), (867.0, 805.0)),((410.0, 768.0), (877.0, 815.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_286.json'), ((1037.24, 390.91), (565.55, 487.76)),((1047.24, 400.91), (575.55, 497.76)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_300.json'), ((434.5, 918.0), (777.0, 694.0)),((444.5, 928.0), (787.0, 704.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_316.json'), ((459.0, 572.0), (811.0, 705.0)),((469.0, 582.0), (821.0, 715.0)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_480.json'), ((582.4, 1178.46), (388.44, 494.98)),((592.4, 1188.46), (398.44, 504.98)))
    True
    >>> is_between(find_correct_rect('contours_json/blood_sugar_341.json'), ((507.5, 671.5), (706.0, 624.0)),((517.5, 681.5), (716.0, 634.0)))
    True
    '''
    
    if include_equal:
        x = v[0][0] <= max(start[0][0], end[0][0]) and v[0][0] >= min(start[0][0], end[0][0])
        y = v[0][1] <= max(start[0][1], end[0][1]) and v[0][1] >= min(start[0][1], end[0][1])
        width = v[1][0] <= max(start[1][0], end[1][0]) and v[1][0] >= min(start[1][0], end[1][0])
        height = v[1][1] <= max(start[1][1], end[1][1]) and v[1][1] >= min(start[1][1], end[1][1])
    else:
        x = v[0][0] < max(start[0][0], end[0][0]) and v[0][0] > min(start[0][0], end[0][0])
        y = v[0][1] < max(start[0][1], end[0][1]) and v[0][1] > min(start[0][1], end[0][1])
        width = v[1][0] < max(start[1][0], end[1][0]) and v[1][0] > min(start[1][0], end[1][0])
        height = v[1][1] < max(start[1][1], end[1][1]) and v[1][1] > min(start[1][1], end[1][1])
    
    return x and y and width and height



if __name__ == '__main__':
    import doctest
    print(doctest.testmod(verbose=False, report=False))