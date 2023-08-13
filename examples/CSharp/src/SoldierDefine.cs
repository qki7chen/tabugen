// This file is auto-generated by Tabugen v0.10.0, DO NOT EDIT!

using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace Config
{
//  兵种.xlsx
public struct SoldierPropertyDefine 
{
    public string Name { get; set; }         // 士兵ID
    public int Level { get; set; }        // 士兵等级
    public string NameID { get; set; }       // 名字
    public string BuildingName { get; set; } // 所属建筑
    public uint BuildingLevel { get; set; } // 建筑等级
    public uint RequireSpace { get; set; } // 登陆艇占用空间
    public uint Volume { get; set; }       // 体积
    public uint UpgradeTime { get; set; }  // 升级消耗的时间(秒）
    public string UpgradeMaterialID { get; set; } // 升级消耗的材料
    public long UpgradeMaterialNum { get; set; } // 升级消耗的数量
    public string ConsumeMaterial { get; set; } // 生产消耗的材料
    public int ConsumeMaterialNum { get; set; } // 生产消耗的数量
    public int ConsumeTime { get; set; }  // 生产消耗的时间（秒/个）
    public int Act { get; set; }          // 攻击
    public int Hp { get; set; }           // 血量
    public short BombLoad { get; set; }     // 载弹量
    public uint Hurt { get; set; }         // buff伤害
    public double Duration { get; set; }     // 持续时间
    public double TriggerInterval { get; set; } // 触发间隔
    public short SearchScope { get; set; }  // 搜索范围
    public double AtkFrequency { get; set; } // 攻击间隔
    public double AtkRange { get; set; }     // 攻击距离
    public double MovingSpeed { get; set; }  // 移动速度
    public bool EnableBurn { get; set; }   // 燃烧特效

    public void ParseFrom(Dictionary<string, string> record) 
    {
        this.Name = record["Name"].Trim();
        this.Level = Utility.ParseInt(record["Level"]);
        this.NameID = record["NameID"].Trim();
        this.BuildingName = record["BuildingName"].Trim();
        this.BuildingLevel = Utility.ParseUInt(record["BuildingLevel"]);
        this.RequireSpace = Utility.ParseUInt(record["RequireSpace"]);
        this.Volume = Utility.ParseUInt(record["Volume"]);
        this.UpgradeTime = Utility.ParseUInt(record["UpgradeTime"]);
        this.UpgradeMaterialID = record["UpgradeMaterialID"].Trim();
        this.UpgradeMaterialNum = Utility.ParseLong(record["UpgradeMaterialNum"]);
        this.ConsumeMaterial = record["ConsumeMaterial"].Trim();
        this.ConsumeMaterialNum = Utility.ParseInt(record["ConsumeMaterialNum"]);
        this.ConsumeTime = Utility.ParseInt(record["ConsumeTime"]);
        this.Act = Utility.ParseInt(record["Act"]);
        this.Hp = Utility.ParseInt(record["Hp"]);
        this.BombLoad = Utility.ParseShort(record["BombLoad"]);
        this.Hurt = Utility.ParseUInt(record["Hurt"]);
        this.Duration = Utility.ParseDouble(record["Duration"]);
        this.TriggerInterval = Utility.ParseDouble(record["TriggerInterval"]);
        this.SearchScope = Utility.ParseShort(record["SearchScope"]);
        this.AtkFrequency = Utility.ParseDouble(record["AtkFrequency"]);
        this.AtkRange = Utility.ParseDouble(record["AtkRange"]);
        this.MovingSpeed = Utility.ParseDouble(record["MovingSpeed"]);
        this.EnableBurn = Utility.ParseBool(record["EnableBurn"]);
    }

}

} // namespace Config 
