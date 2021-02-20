// This file is auto-generated by Tabular v1.4.0, DO NOT EDIT!

package com.mycompany.csvconfig;

import java.util.*;
import java.io.IOException;
import org.apache.commons.csv.*;

// 全局数值配置, 全局变量表.xlsx
public class GlobalPropertyDefine
{
    public double               GoldExchangeTimeFactor1 = 0.0f;    // 金币兑换时间参数1
    public double               GoldExchangeTimeFactor2 = 0.0f;    // 金币兑换时间参数2
    public double               GoldExchangeTimeFactor3 = 0.0f;    // 金币兑换时间参数3
    public short                GoldExchangeResource1Price = 0;    // 金币兑换资源1价格
    public short                GoldExchangeResource2Price = 0;    // 金币兑换资源2价格
    public short                GoldExchangeResource3Price = 0;    // 金币兑换资源3价格
    public short                GoldExchangeResource4Price = 0;    // 金币兑换资源4价格
    public short                FreeCompleteSeconds = 0;           // 免费立即完成时间
    public short                CancelBuildReturnPercent = 0;      // 取消建造后返还资源比例
    public boolean              EnableSearch = false;              // 开启搜索
    public int[]                SpawnLevelLimit = null;            // 最大刷新个数显示
    public Map<String,Integer>  FirstRechargeReward = new HashMap<>(); // 首充奖励

    // parse fields data from text records
    public void parseFrom(List<CSVRecord> records)
    {
        if (records.size() < 12) {
            throw new RuntimeException(String.format("GlobalPropertyDefine: records length too short, %d < 12", records.size()));
        }
        if (!records.get(0).get(2).isEmpty()) {
            this.GoldExchangeTimeFactor1 = Double.parseDouble(records.get(0).get(2));
        }
        if (!records.get(1).get(2).isEmpty()) {
            this.GoldExchangeTimeFactor2 = Double.parseDouble(records.get(1).get(2));
        }
        if (!records.get(2).get(2).isEmpty()) {
            this.GoldExchangeTimeFactor3 = Double.parseDouble(records.get(2).get(2));
        }
        if (!records.get(3).get(2).isEmpty()) {
            this.GoldExchangeResource1Price = Short.parseShort(records.get(3).get(2));
        }
        if (!records.get(4).get(2).isEmpty()) {
            this.GoldExchangeResource2Price = Short.parseShort(records.get(4).get(2));
        }
        if (!records.get(5).get(2).isEmpty()) {
            this.GoldExchangeResource3Price = Short.parseShort(records.get(5).get(2));
        }
        if (!records.get(6).get(2).isEmpty()) {
            this.GoldExchangeResource4Price = Short.parseShort(records.get(6).get(2));
        }
        if (!records.get(7).get(2).isEmpty()) {
            this.FreeCompleteSeconds = Short.parseShort(records.get(7).get(2));
        }
        if (!records.get(8).get(2).isEmpty()) {
            this.CancelBuildReturnPercent = Short.parseShort(records.get(8).get(2));
        }
        if (!records.get(9).get(2).isEmpty()) {
            this.EnableSearch = AutogenConfigManager.parseBool(records.get(9).get(2));
        }
        {
            String[] kvList = records.get(10).get(2).split(AutogenConfigManager.TAB_ARRAY_DELIM);
            int[] list = new int[kvList.length];
            for (int i = 0; i < kvList.length; i++) {
                if (!kvList[i].isEmpty()) {
                    int value = Integer.parseInt(kvList[i]);
                    list[i] = value;
                }
            }
            this.SpawnLevelLimit = list;
        }
        {
            String[] kvList = records.get(11).get(2).split(AutogenConfigManager.TAB_MAP_DELIM1);
            for(int i = 0; i < kvList.length; i++) {
                String text = kvList[i];
                if (text.isEmpty()) {
                    continue;
                }
                String[] item = text.split(AutogenConfigManager.TAB_MAP_DELIM2);
                String key = item[0].trim();
                int value = Integer.parseInt(item[1]);
                this.FirstRechargeReward.put(key, value);
            }
        }
    }
}
