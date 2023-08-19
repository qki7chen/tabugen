// This file is auto-generated by Tabugen v0.10.0, DO NOT EDIT!

package com.pdfun.config;

import java.util.*;

//  新手任务.xlsx
public class NewbieGuideDefine 
{
    public String               Name = "";             // ID
    public String               Type = "";             // 任务类型
    public String               Target = "";           // 目标
    public short[]              Accomplishment = null; // 完成步骤
    public Map<String,Integer>  Goods = null;          // 物品

    public void parseFrom(Map<String, String> record) 
    {
        this.Name = record.get("Name");
        this.Type = record.get("Type");
        this.Target = record.get("Target");
        this.Accomplishment = Conv.parseShortArray(record.get("Accomplishment"));
        this.Goods = Conv.parseMap(record.get("Goods"), String.class, Integer.class);
    }

}
