// This file is auto-generated by Tabugen v0.5.0, DO NOT EDIT!

using System;
using System.IO;
using System.Collections.Generic;

namespace Config
{

// 新手引导配置, 新手任务.xlsx
public class NewbieGuideDefine
{
    public string                    Name = "";             // ID
    public string                    Type = "";             // 任务类型
    public string                    Target = "";           // 目标
    public short[]                   Accomplishment = null; // 完成步骤
    public Dictionary<string, uint>  Goods = null;          // 物品
    public string                    Description = "";      // 描述

    // parse object fields from a text row
    public void ParseFromRow(List<string> row)
    {
        if (row.Count < 6) {
            throw new ArgumentException(string.Format("NewbieGuideDefine: row length too short {0}", row.Count));
        }
        if (row[0].Length > 0) {
            this.Name = row[0].Trim();
        }
        if (row[1].Length > 0) {
            this.Type = row[1].Trim();
        }
        if (row[2].Length > 0) {
            this.Target = row[2].Trim();
        }
        {
            var items = row[3].Split(AutogenConfigManager.TABUGEN_ARRAY_DELIM, StringSplitOptions.RemoveEmptyEntries);
            this.Accomplishment = new short[items.Length];
            for(int i = 0; i < items.Length; i++) 
            {
                var value = short.Parse(items[i]);
                this.Accomplishment[i] = value;
            }
        }
        {
            var items = row[4].Split(AutogenConfigManager.TABUGEN_MAP_DELIM1, StringSplitOptions.RemoveEmptyEntries);
            this.Goods = new Dictionary<string,uint>();
            for(int i = 0; i < items.Length; i++) 
            {
                string text = items[i];
                if (text.Length == 0) {
                    continue;
                }
                var item = text.Split(AutogenConfigManager.TABUGEN_MAP_DELIM2, StringSplitOptions.RemoveEmptyEntries);
                if (items.Length == 2) {
                var key = item[0].Trim();
                var value = uint.Parse(item[1]);
                    this.Goods[key] = value;
                }
            }
        }
        if (row[5].Length > 0) {
            this.Description = row[5].Trim();
        }
    }
}


public class AutogenConfigManager 
{    
    public const char TABUGEN_CSV_SEP = ',';           // CSV field delimiter
    public const char TABUGEN_CSV_QUOTE = '"';          // CSV field quote
    public const char TABUGEN_ARRAY_DELIM = ',';       // array item delimiter
    public const char TABUGEN_MAP_DELIM1 = ';';        // map item delimiter
    public const char TABUGEN_MAP_DELIM2 = '=';        // map key-value delimiter
    

    public static bool ParseBool(string text)
    {
        if (text.Length > 0)
        {
            return string.Equals(text, "1") ||
                string.Equals(text, "y", StringComparison.OrdinalIgnoreCase) ||
                string.Equals(text, "on", StringComparison.OrdinalIgnoreCase) ||
                string.Equals(text, "yes", StringComparison.OrdinalIgnoreCase) ||
                string.Equals(text, "true", StringComparison.OrdinalIgnoreCase);
        }
        return false;
    }

    // 读取文件内容
    public static string ReadFileContent(string filepath)
    {
        StreamReader reader = new StreamReader(filepath);
        return reader.ReadToEnd();
    }
    
    // 把内容分行
    public static List<string> ReadTextToLines(string content)
    {
        List<string> lines = new List<string>();
        using (StringReader reader = new StringReader(content))
        {
            string line;
            while ((line = reader.ReadLine()) != null)
            {
                lines.Add(line);
            }
        }
        return lines;
    }

    // 从一行读取record
    public static List<string> ReadRecordFromLine(string line)
    {
        List<string> row = new List<string>();
        int pos = 0;
        while (pos < line.Length)
        {
            string field = "";
            pos = ParseNextColumn(line, pos, out field);
            row.Add(field.Trim());
            if (pos < 0)
            {
                break;
            }
        }
        return row;
    }
        
    // 解析下一个column
    public static int ParseNextColumn(string line, int start, out string field)
    {
        bool in_quote = false;
        if (line[start] == TABUGEN_CSV_QUOTE)
        {
            in_quote = true;
            start++;
        }
        int pos = start;
        for (; pos < line.Length; pos++)
        {
            if (in_quote && line[pos] == TABUGEN_CSV_QUOTE)
            {
                if (pos + 1 < line.Length && line[pos + 1] == TABUGEN_CSV_SEP)
                {
                    field = line.Substring(start, pos - start);
                    return pos + 2;
                }
                else
                {
                    field = line.Substring(start, pos - start);
                    return pos + 1;
                }
            }
            if (!in_quote && line[pos] == TABUGEN_CSV_SEP)
            {
                field = line.Substring(start, pos - start);
                return pos + 1;
            }
        }
        field = line.Substring(start, pos);
        return -1;
    }
}


}
