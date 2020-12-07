// This file is auto-generated by Tabular v1.4.0, DO NOT EDIT!

#include "AutogenConfig.h"
#include <stddef.h>
#include <assert.h>
#include <memory>
#include <fstream>
#include "Utility/Conv.h"
#include "Utility/StringUtil.h"
#include "Utility/CSVReader.h"

using namespace std;

#ifndef ASSERT
#define ASSERT assert
#endif


namespace config
{


std::function<std::string(const char*)> AutogenConfigManager::reader = AutogenConfigManager::ReadFileContent;

namespace 
{
    static std::vector<SoldierPropertyDefine>* _instance_soldierpropertydefine = nullptr;
}

void AutogenConfigManager::LoadAll()
{
    ASSERT(reader);
    SoldierPropertyDefine::Load("soldier_property_define.csv");
}

void AutogenConfigManager::ClearAll()
{
    delete _instance_soldierpropertydefine;
    _instance_soldierpropertydefine = nullptr;
}


//Load content of an asset file'
std::string AutogenConfigManager::ReadFileContent(const char* filepath)
{
    ASSERT(filepath != nullptr);
    FILE* fp = std::fopen(filepath, "rb");
    if (fp == NULL) {
        return "";
    }
    fseek(fp, 0, SEEK_END);
    long size = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    if (size == 0) {
        fclose(fp);
        return "";
    }
    std::string content;
    fread(&content[0], 1, size, fp);
    fclose(fp);
    return std::move(content);
}


const std::vector<SoldierPropertyDefine>* SoldierPropertyDefine::GetData()
{
    ASSERT(_instance_soldierpropertydefine != nullptr);
    return _instance_soldierpropertydefine;
}


const SoldierPropertyDefine* SoldierPropertyDefine::Get(const std::string& Name, int Level)
{
    const vector<SoldierPropertyDefine>* dataptr = GetData();
    ASSERT(dataptr != nullptr && dataptr->size() > 0);
    for (size_t i = 0; i < dataptr->size(); i++)
    {
        if (dataptr->at(i).Name == Name && dataptr->at(i).Level == Level)
        {
            return &dataptr->at(i);
        }
    }
    return nullptr;
}

std::vector<const SoldierPropertyDefine*> SoldierPropertyDefine::GetRange(const std::string& Name)
{
    const vector<SoldierPropertyDefine>* dataptr = GetData();
    std::vector<const SoldierPropertyDefine*> range;
    ASSERT(dataptr != nullptr && dataptr->size() > 0);
    for (size_t i = 0; i < dataptr->size(); i++)
    {
        if (dataptr->at(i).Name == Name)
        {
            range.push_back(&dataptr->at(i));
        }
    }
    return range;
}

// load SoldierPropertyDefine data from csv file
int SoldierPropertyDefine::Load(const char* filepath)
{
    vector<SoldierPropertyDefine>* dataptr = new vector<SoldierPropertyDefine>;
    std::string content = AutogenConfigManager::reader(filepath);
    CSVReader reader(TAB_CSV_SEP, TAB_CSV_QUOTE);
    reader.Parse(content);
    auto rows = reader.GetRows();
    ASSERT(!rows.empty());
    for (size_t i = 0; i < rows.size(); i++)
    {
        auto row = rows[i];
        if (!row.empty())
        {
            SoldierPropertyDefine item;
            SoldierPropertyDefine::ParseFromRow(row, &item);
            dataptr->push_back(item);
        }
    }
    delete _instance_soldierpropertydefine;
    _instance_soldierpropertydefine = dataptr;
    return 0;
}

// parse data object from an csv row
int SoldierPropertyDefine::ParseFromRow(const vector<StringPiece>& row, SoldierPropertyDefine* ptr)
{
    ASSERT(row.size() >= 25);
    ASSERT(ptr != nullptr);
    ptr->Name = ParseTextAs<std::string>(row[0]);
    ptr->Level = ParseTextAs<int>(row[1]);
    ptr->NameID = ParseTextAs<std::string>(row[2]);
    ptr->Description = ParseTextAs<std::string>(row[3]);
    ptr->BuildingName = ParseTextAs<std::string>(row[4]);
    ptr->BuildingLevel = ParseTextAs<uint32_t>(row[5]);
    ptr->RequireSpace = ParseTextAs<uint32_t>(row[6]);
    ptr->Volume = ParseTextAs<uint32_t>(row[7]);
    ptr->UpgradeTime = ParseTextAs<uint32_t>(row[8]);
    ptr->UpgradeMaterialID = ParseTextAs<std::string>(row[9]);
    ptr->UpgradeMaterialNum = ParseTextAs<int64_t>(row[10]);
    ptr->ConsumeMaterial = ParseTextAs<std::string>(row[11]);
    ptr->ConsumeMaterialNum = ParseTextAs<int>(row[12]);
    ptr->ConsumeTime = ParseTextAs<int>(row[13]);
    ptr->Act = ParseTextAs<int>(row[14]);
    ptr->Hp = ParseTextAs<int>(row[15]);
    ptr->Hurt = ParseTextAs<uint32_t>(row[17]);
    ptr->SearchScope = ParseTextAs<int16_t>(row[20]);
    ptr->AtkFrequency = ParseTextAs<float>(row[21]);
    ptr->AtkRange = ParseTextAs<double>(row[22]);
    ptr->MovingSpeed = ParseTextAs<double>(row[23]);
    ptr->EnableBurn = ParseTextAs<bool>(row[24]);
    return 0;
}


} // namespace config 
