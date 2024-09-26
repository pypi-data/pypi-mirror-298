#!/usr/bin/env python3

import datetime

import VisualLog.LogParser as LogParser
import VisualLog.MatplotlibZoom as MatplotlibZoom

import matplotlib.pyplot as plot
from matplotlib.figure import Figure
from matplotlib.axes import Axes

class VisualLogPlot:
    """
    VisualLogPlot

    暂时不知道为什么Qt直接引用VisualLog、matplotlib会导致界面上的下拉框界面出问题，所以采用反射来处理解决
    """

    def __init__(self, kwargs):
        print("VisualLogPlot")

        # 清理matplotlib相关绘图，防止出现未知异常报错
        plot.close()
        if kwargs["plotType"] == "normal":
            MatplotlibZoom.Show(callback=VisualLogPlot.defaultShowCallback, rows = 1, cols = 1, args=kwargs)
        elif kwargs["plotType"] == "key":
            MatplotlibZoom.Show(callback=VisualLogPlot.defaultKeyShowCallback, rows = 1, cols = 1, args=kwargs)
        elif kwargs["plotType"] == "keyLoop":
            MatplotlibZoom.Show(callback=VisualLogPlot.defaultKeyLoopShowCallback, rows = 1, cols = 1, args=kwargs)
        else:
            print("unsupport plot type")

    @classmethod
    def defaultKeyLoopShowCallback(clz, fig: Figure, index, args):
        '''
        目前只支持单文件数据循环绘制

        xAxis: 需要是字符串索引，只取第一个
        dataIndex: 需要时float索引，只取第一个
        '''

        ax: Axes = fig.get_axes()[index]
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        visualLogData = args

        if len(args["lineInfosFiles"]) != 1:
            return

        if len(visualLogData["xAxis"]) == 0 or len(visualLogData["dataIndex"]) == 0:
            print("please set x,y index")

            return

        # get keys
        keys = []
        keyIndex = visualLogData["xAxis"][0]
        valueIndex = visualLogData["dataIndex"][0]

        print(keyIndex)
        print(valueIndex)
        print(args["lineInfosFiles"])
        # 迭代文件
        for lineInfos in args["lineInfosFiles"]:
            if len(lineInfos) == 0:
                continue

            # 单个数组
            for info in lineInfos:
                if isinstance(info[keyIndex], str) and (not isinstance(info[valueIndex], str)):
                    if info[keyIndex] not in keys:
                        keys.append(info[keyIndex])
                else:
                    return

        print(keys)

        curveIndex = 1
        plotY = None
        plotYs = []
        for lineInfos in args["lineInfosFiles"]:
            if len(lineInfos) == 0:
                continue

            # 单个数组，每组key对应的值取第一个，防止重复
            plotY = []
            relativeI = 0
            dataLength = len(lineInfos)
            for i in range(dataLength):
                info = lineInfos[i]
                if info[keyIndex] == keys[0]:
                    plotY = []
                    relativeI = i

                if info[keyIndex] in keys:
                    if (isinstance(info[valueIndex], datetime.datetime)):
                        dateInfo: datetime.datetime = info[valueIndex]
                        if len(plotY) == 0:
                            plotY.append(0.0)
                        else:
                            plotY.append(dateInfo.timestamp() - lineInfos[relativeI][valueIndex].timestamp())

                    else:
                        plotY.append(info[valueIndex] - lineInfos[relativeI][valueIndex])

                if info[keyIndex] == keys[-1]:
                    plotYs.append(plotY)

            print(plotYs)
            for i in range(len(plotYs)):
                for item_index in range(len(plotYs[i])):
                    # 画点
                    ax.plot(item_index, plotYs[i][item_index], 'o')
                    # 画垂线
                    ax.plot([item_index, item_index], [0, plotYs[i][item_index]], color="gray")
                # 画连线
                ax.plot(range(len(plotYs[i])), plotYs[i], label="curve " + str(curveIndex))

            curveIndex += 1

        # 写文字
        for item_index in range(len(keys)):
            ax.text(item_index, plotYs[0][item_index] + 1, list(keys)[item_index], fontsize=7, rotation=90)

        ax.legend()

    @classmethod
    def defaultKeyShowCallback(clz, fig: Figure, index, args):
        '''
        目前只支持两条曲线绘制对比

        xAxis: 需要是字符串索引，只取第一个
        dataIndex: 需要时float索引，只取第一个
        '''

        ax: Axes = fig.get_axes()[index]
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        visualLogData = args

        if len(args["lineInfosFiles"]) == 0:
            return

        if len(visualLogData["xAxis"]) == 0 or len(visualLogData["dataIndex"]) == 0:
            print("please set x,y index")

            return

        # get keys
        keys = []
        keyIndex = visualLogData["xAxis"][0]
        valueIndex = visualLogData["dataIndex"][0]

        print(keyIndex)
        print(valueIndex)
        print(args["lineInfosFiles"])
        # 迭代文件
        for lineInfos in args["lineInfosFiles"]:
            if len(lineInfos) == 0:
                continue

            # 单个数组
            for info in lineInfos:
                if isinstance(info[keyIndex], str) and (not isinstance(info[valueIndex], str)):
                    if info[keyIndex] not in keys:
                        keys.append(info[keyIndex])
                else:
                    return

        print(keys)

        curveIndex = 1
        plotY = None
        plotYs = []
        for lineInfos in args["lineInfosFiles"]:
            if len(lineInfos) == 0:
                continue

            # 单个数组，每组key对应的值取第一个，防止重复
            plotY = []
            for key in keys:
                '''
                for info in lineInfos:
                    if info[keyIndex] == key:
                        plotY.append(info[valueIndex])

                        break
                '''
                dataLength = len(lineInfos)
                for i in range(dataLength):
                    info = lineInfos[i]
                    if info[keyIndex] == key:
                        if (isinstance(info[valueIndex], datetime.datetime)):
                            dateInfo: datetime.datetime = info[valueIndex]
                            if i == 0:
                                plotY.append(0.0)
                            else:
                                plotY.append(dateInfo.timestamp() - lineInfos[0][valueIndex].timestamp())

                        else:
                            plotY.append(info[valueIndex])

                        break

                    # 没找到就用前面一个填充
                    if i == (dataLength - 1):
                        plotY.append(plotY[-1])

            print(plotY)
            for item_index in range(len(plotY)):
                # 画点
                ax.plot(item_index, plotY[item_index], 'o')
                # 画垂线
                ax.plot([item_index, item_index], [0, plotY[item_index]], color="gray")
            # 画连线
            ax.plot(range(len(plotY)), plotY, label="curve " + str(curveIndex))

            curveIndex += 1
            plotYs.append(plotY)

        # 写文字
        for item_index in range(len(keys)):
            ax.text(item_index, plotY[item_index] + 1, list(keys)[item_index], fontsize=7, rotation=90)

        if len(plotYs) == 2:
            # 计算差分，画差分
            diffY = []
            incrementY = []
            for i in range(len(keys)):
                diffY.append(plotYs[1][i] - plotYs[0][i])

                if i == 0:
                    incrementY.append(diffY[0])
                else:
                    incrementY.append(diffY[i] - diffY[i - 1])
            ax.plot(range(len(keys)), diffY, label="curve diff")
            ax.plot(range(len(keys)), incrementY, label="curve increment")

        ax.legend()

    @classmethod
    def defaultShowCallback(clz, fig: Figure, index, args):
        """
        默认绘图方式

        args:

        {
            'xAxis': [0],               # x轴，支持int/float/datetime
            'dataIndex': [1],           # y轴，支持init/float/str
            'lineInfosFiles': [
                [file data],
                [file data]
            ]
        }
        """

        # https://matplotlib.org/stable/api/
        ax: Axes = fig.get_axes()[index]
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        visualLogData = args

        if len(args["lineInfosFiles"]) == 0:
            return

        for lineInfos in args["lineInfosFiles"]:
            if len(lineInfos) == 0:
                continue

            # print(lineInfos[0])
            if len(visualLogData["xAxis"]) > 0:
                # 迭代第一行数据，相当于绘制多少条线，每一列相当于一条线，一行数据中由x轴和y轴组成
                #   1. i表示当前绘制第几条线
                #   2. x表示当前当前x轴索引
                for i in range(len(lineInfos[0])):
                    if i in visualLogData["dataIndex"]:
                        # 迭代x轴，主要是获取x轴索引，相当于用第j个x轴绘制第i个y轴
                        for j in range(len(visualLogData["xAxis"])):
                            x = visualLogData["xAxis"][j]                                               # 获取x索引
                            if (i == x) and (x in visualLogData["dataIndex"]):                          # 处理针对X轴绘图
                                # i == x的会进入这个if，但是数组长度不同不会处理
                                # datetime模式，只以日期为X轴，Y轴表示当前计数，正常的模式下X轴不处理
                                # if isinstance(lineInfos[0][i], datetime.datetime) and len(visualLogData["xAxis"]) == len(lineInfos[0]):
                                if isinstance(lineInfos[0][i], datetime.datetime) and len(visualLogData["dataIndex"]) == 1:
                                    pointCount = 0

                                    for s in lineInfos:
                                        pointCount += 1

                                        # 文字
                                        ax.text(s[x], pointCount + 0.2, str(pointCount), fontsize=9)
                                        # 圆点
                                        ax.plot(s[x], pointCount, 'o')
                                        # 虚线
                                        ax.plot([s[x], s[x]], [pointCount, 0], linestyle = 'dotted')
                            else:                                                                       # 用X轴索引数据绘制Y轴
                                # dataIndex表示必须要绘制的图，不一定包括X轴
                                if (i in visualLogData["dataIndex"]):
                                    # if
                                    #     绘制垂直线
                                    # else
                                    #     不绘制垂直线
                                    if isinstance(lineInfos[0][i], str):
                                        pointCount = 1

                                        for s in lineInfos:
                                            pointCount += 1

                                            # 文字
                                            ax.text(s[x], pointCount + 0.2, s[i], fontsize=9, rotation=90)
                                            # 圆点
                                            ax.plot(s[x], pointCount, 'o')
                                            # 虚线
                                            ax.plot([s[x], s[x]], [pointCount, 0], linestyle = 'dotted')
                                    else:
                                        ax.plot([s[x] for s in lineInfos], [s[i] for s in lineInfos])
                                        for s in lineInfos:
                                            ax.plot(s[x], s[i], 'o')

                                # 处理针对X轴绘制垂直线
                                if (x in visualLogData["dataIndex"]):
                                    for s in lineInfos:
                                        ax.plot([s[x], s[x]], [s[i], 0], linestyle = 'dotted')
            else:
                # 迭代第一行数据，相当于绘制多少条线，每一列相当于一条线
                for i in range(len(lineInfos[0])):
                    if i in visualLogData["dataIndex"]:
                        # ax.plot(range(len(lineInfos)), [s[i] for s in lineInfos], label = labels[i])
                        ax.plot(range(len(lineInfos)), [s[i] for s in lineInfos])

        ax.legend()

    def parseData(filePath, regex):
        print("parseData")

        return LogParser.logFileParser(
            filePath,
            regex
        )
