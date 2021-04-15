// This file is auto-generated by Tabular v0.6.1, DO NOT EDIT!

package com.mycompany.csvconfig;

import java.util.*;
import java.io.IOException;
import org.apache.commons.csv.*;

// 新手引导配置, 新手任务.xlsx
public class NewbieGuideDefine
{
    public String               Name = "";             // ID
    public String               Type = "";             // 任务类型
    public String               Target = "";           // 目标
    public short[]              Accomplishment = null; // 完成步骤
    public Map<String,Integer>  Goods = new HashMap<>(); // 物品
    public String               Description = "";      // 描述

    // parse fields data from record
    public void parseFrom(CSVRecord record)
    {
        if (record.size() < 6) {
            throw new RuntimeException(String.format("NewbieGuideDefine: record length too short %d", record.size()));
        }
        if (!record.get(0).isEmpty()) {
            this.Name = record.get(0).trim();
        }
        if (!record.get(1).isEmpty()) {
            this.Type = record.get(1).trim();
        }
        if (!record.get(2).isEmpty()) {
            this.Target = record.get(2).trim();
        }
        {
            String[] kvList = record.get(3).split(AutogenConfigManager.TABULAR_ARRAY_DELIM);
            short[] list = new short[kvList.length];
            for (int i = 0; i < kvList.length; i++) {
                if (!kvList[i].isEmpty()) {
                    short value = Short.parseShort(kvList[i]);
                    list[i] = value;
                }
            }
            this.Accomplishment = list;
        }
        {
            String[] kvList = record.get(4).split(AutogenConfigManager.TABULAR_MAP_DELIM1);
            for(int i = 0; i < kvList.length; i++) {
                String text = kvList[i];
                if (text.isEmpty()) {
                    continue;
                }
                String[] item = text.split(AutogenConfigManager.TABULAR_MAP_DELIM2);
                String key = item[0].trim();
                int value = Integer.parseInt(item[1]);
                this.Goods.put(key, value);
            }
        }
        if (!record.get(5).isEmpty()) {
            this.Description = record.get(5).trim();
        }
    }
}
