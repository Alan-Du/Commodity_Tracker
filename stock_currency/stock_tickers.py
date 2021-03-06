# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 01:37:09 2020
Get Historical stock price data and upload into DB
@author: Shaolun du
@contact: Shaolun.du@gmail.com
"""
stock_tickers = [ '600219.SS', '600876.SS', '600515.SS', '300003.SZ', 
                  '600036.SS', '002087.SZ', '600115.SS', '000564.SZ', 
                  '600100.SS', '600586.SS', '002013.SZ', '300454.SZ', 
                  '688036.SS', '603733.SS', '600722.SS', '000825.SZ', 
                  '002237.SZ', '601998.SS', '002506.SZ', '600583.SS', 
                  '000848.SZ', '002422.SZ', '601298.SS', '000735.SZ', 
                  '601939.SS', '002100.SZ', '002961.SZ', '601368.SS', 
                  '002271.SZ', '603766.SS', '002648.SZ', '600030.SS', 
                  '600773.SS', '002268.SZ', '002768.SZ', '603983.SS', 
                  '002134.SZ', '603618.SS', '601225.SS', '002563.SZ', 
                  '603160.SS', '000703.SZ', '000702.SZ', '000723.SZ', 
                  '002042.SZ', '600029.SS', '000002.SZ', '002109.SZ', 
                  '300770.SZ', '600887.SS', '603369.SS', '000651.SZ', 
                  '000585.SZ', '601166.SS', '600705.SS', '000936.SZ', 
                  '000505.SZ', '600118.SS', '002234.SZ', '600901.SS', 
                  '002735.SZ', '002568.SZ', '601898.SS', '601211.SS', 
                  '002267.SZ', '000158.SZ', '000596.SZ', '600847.SS', 
                  '002607.SZ', '002186.SZ', '601336.SS', '000708.SZ', 
                  '002377.SZ', '000983.SZ', '600532.SS', '001965.SZ', 
                  '600196.SS', '002293.SZ', '600867.SS', '002832.SZ', 
                  '000635.SZ', '002498.SZ', '002243.SZ', '601012.SS', 
                  '000911.SZ', '002127.SZ', '002739.SZ', '002565.SZ', 
                  '600664.SS', '601319.SS', '600740.SS', '601020.SS', 
                  '603883.SS', '300750.SZ', '000751.SZ', '000768.SZ',
                  '300761.SZ', '002212.SZ', '601015.SS', '000683.SZ', 
                  '600157.SS', '002419.SZ', '601877.SS', '600266.SS', 
                  '000963.SZ', '600126.SS', '601677.SS', '002024.SZ', 
                  '600010.SS', '603589.SS', '601919.SS', '600816.SS', 
                  '002493.SZ', '002080.SZ', '603328.SS', '600777.SS', 
                  '600338.SS', '601288.SS', '002179.SZ', '601328.SS', 
                  '600104.SS', '600332.SS', '603288.SS', '600295.SS', 
                  '300189.SZ', '300142.SZ', '002557.SZ', '600837.SS', 
                  '300766.SZ', '300033.SZ', '300177.SZ', '603988.SS', 
                  '601339.SS', '600027.SS', '002423.SZ', '600066.SS', 
                  '600511.SS', '002153.SZ', '300759.SZ', '002180.SZ', 
                  '000063.SZ', '000021.SZ', '002286.SZ', '000859.SZ', 
                  '002451.SZ', '600377.SS', '600893.SS', '002522.SZ', 
                  '000568.SZ', '000726.SZ', '002916.SZ', '603993.SS', 
                  '601111.SS', '600548.SS', '600018.SS', '000997.SZ', 
                  '000961.SZ', '600795.SS', '600776.SS', '600127.SS', 
                  '002466.SZ', '600845.SS', '601872.SS', '002242.SZ', 
                  '603619.SS', '600988.SS', '002014.SZ', '600436.SS', 
                  '601636.SS', '000333.SZ', '603606.SS', '001872.SZ', 
                  '600637.SS', '002114.SZ', '600600.SS', '002471.SZ', 
                  '002252.SZ', '002812.SZ', '603517.SS', '603156.SS', 
                  '601958.SS', '000688.SZ', '002157.SZ', '603501.SS', 
                  '601005.SS', '002741.SZ', '603888.SS', '002073.SZ', 
                  '000878.SZ', '600733.SS', '000001.SZ', '600803.SS', 
                  '600585.SS', '600048.SS', '300294.SZ', '300741.SZ', 
                  '600903.SS', '000898.SZ', '600299.SS', '601992.SS', 
                  '600011.SS', '000968.SZ', '002318.SZ', '000977.SZ', 
                  '600023.SS', '000921.SZ', '600482.SS', '000923.SZ', 
                  '601168.SS', '300498.SZ', '600500.SS', '002727.SZ', 
                  '300015.SZ', '002911.SZ', '601139.SS', '300357.SZ', 
                  '603021.SS', '002628.SZ', '600009.SS', '601828.SS', 
                  '300413.SZ', '600300.SS', '000869.SZ', '601789.SS', 
                  '002705.SZ', '000028.SZ', '002078.SZ', '600681.SS', 
                  '600191.SS', '600221.SS', '002050.SZ', '002233.SZ', 
                  '601333.SS', '600019.SS', '000959.SZ', '000937.SZ', 
                  '600584.SS', '603868.SS', '600763.SS', '600966.SS', 
                  '002201.SZ', '603019.SS', '000895.SZ', '600008.SS', 
                  '600859.SS', '601727.SS', '601628.SS', '300408.SZ', 
                  '000627.SZ', '600819.SS', '603986.SS', '600521.SS', 
                  '002224.SZ', '600170.SS', '601869.SS', '600635.SS', 
                  '002602.SZ', '600897.SS', '002202.SZ', '002327.SZ', 
                  '000786.SZ', '002128.SZ', '600737.SS', '300308.SZ', 
                  '601021.SS', '002032.SZ', '002511.SZ', '600426.SS', 
                  '601699.SS', '601088.SS', '600570.SS', '600166.SS', 
                  '600977.SS', '600962.SS', '002585.SZ', '002508.SZ', 
                  '000488.SZ', '601118.SS', '300676.SZ', '603659.SS', 
                  '601233.SS', '000498.SZ', '600487.SS', '002092.SZ', 
                  '600308.SS', '600050.SS', '601398.SS', '603259.SS', 
                  '300135.SZ', '601318.SS', '300577.SZ', '002463.SZ', 
                  '600759.SS', '603587.SS', '002110.SZ', '300208.SZ', 
                  '600125.SS', '300251.SZ', '600372.SS', '600873.SS', 
                  '603885.SS', '600117.SS', '600415.SS', '601311.SS', 
                  '002152.SZ', '002381.SZ', '600315.SS', '002578.SZ', 
                  '600020.SS', '600588.SS', '600968.SS', '000938.SZ', 
                  '002230.SZ', '000538.SZ', '600963.SS', '600869.SS', 
                  '300428.SZ', '601601.SS', '002732.SZ', '600497.SS', 
                  '000612.SZ', '000721.SZ', '600089.SS', '002601.SZ', 
                  '300146.SZ', '000661.SZ', '300628.SZ', '600350.SS', 
                  '600340.SS', '600973.SS', '601688.SS', '600276.SS', 
                  '601607.SS', '601216.SS', '000066.SZ', '600111.SS', 
                  '600251.SS', '300093.SZ', '000576.SZ', '600398.SS', 
                  '002299.SZ', '002307.SZ', '600160.SS', '600872.SS', 
                  '600519.SS', '002558.SZ', '600406.SS', '600269.SS', 
                  '600827.SS', '000860.SZ', '601633.SS', '000429.SZ', 
                  '300122.SZ', '601988.SS', '002208.SZ', '600606.SS', 
                  '600917.SS', '002007.SZ', '300760.SZ', '000850.SZ', 
                  '000301.SZ', '600489.SS', '000426.SZ', '600547.SS', 
                  '000807.SZ', '000089.SZ', '603936.SS', '601991.SS', 
                  '600438.SS', '000599.SZ', '603858.SS', '002594.SZ', 
                  '000069.SZ', '002067.SZ', '601718.SS', '000933.SZ', 
                  '600085.SS', '601969.SS', '603920.SS', '600208.SS', 
                  '600507.SS', '002938.SZ', '600567.SS', '300017.SZ', 
                  '002002.SZ', '000639.SZ', '000625.SZ', '002304.SZ', 
                  '600875.SS', '601933.SS', '600004.SS', '002624.SZ', 
                  '300526.SZ', '300113.SZ', '002276.SZ', '300221.SZ', 
                  '603711.SS', '600056.SS', '600352.SS', '000709.SZ', 
                  '600660.SS', '603113.SS', '600469.SS', '000655.SZ', 
                  '600183.SS', '600177.SS', '603799.SS', '600390.SS', 
                  '600959.SS', '688008.SS', '300347.SZ', '600498.SS', 
                  '002311.SZ', '000882.SZ', '601066.SS', '002211.SZ', 
                  '601158.SS', '600989.SS', '600695.SS', '603233.SS', 
                  '600801.SS', '600581.SS', '600368.SS', '600400.SS', 
                  '000960.SZ', '000550.SZ', '000589.SZ', '601360.SS', 
                  '000876.SZ', '600808.SS', '002372.SZ', '600985.SS', 
                  '300027.SZ', '601989.SS', '002852.SZ', '601238.SS', 
                  '603668.SS', '600809.SS', '601006.SS', '603000.SS', 
                  '600871.SS', '300783.SZ', '002555.SZ', '600362.SS', 
                  '600239.SS', '002001.SZ', '002589.SZ', '600339.SS', 
                  '002155.SZ', '601155.SS', '000782.SZ', '600820.SS', 
                  '000001.SS', '600161.SS', '300383.SZ', '000012.SZ', 
                  '600150.SS', '600143.SS', '603486.SS', '603866.SS', 
                  '002302.SZ', '002123.SZ', '001979.SZ', '000800.SZ', 
                  '600210.SS', '600318.SS', '600090.SS', '600188.SS', 
                  '600690.SS', '000553.SZ', '601698.SS', '600284.SS', 
                  '601857.SS', '600176.SS', '600146.SS', '600000.SS', 
                  '000420.SZ', '002027.SZ', '002044.SZ', '000630.SZ', 
                  '600103.SS', '600409.SS', '601600.SS', '603939.SS', 
                  '600540.SS', '600383.SS', '600346.SS', '600618.SS', 
                  '601808.SS', '600783.SS', '600961.SS', '603878.SS'
                  ]

