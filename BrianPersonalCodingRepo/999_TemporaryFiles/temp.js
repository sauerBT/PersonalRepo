if (msg.payload.entity_id == "climate.ecobee4thermostat") {

    var mqttRetainMode = "false"
    var mqttQosMode = 2
    var prefixTopic = flow.get("TopicStr")
    var deviceName = "ecobee4thermostat"
    var topicHvacMode = prefixTopic + "/" + deviceName + "/Edge/hvacMode"
    var topicMinTemp = prefixTopic + "/" + deviceName + "/Edge/minTemp"
    var topicMaxTemp = prefixTopic + "/" + deviceName + "/Edge/maxTemp"
    var topicTargetTempHI = prefixTopic + "/" + deviceName + "/Edge/TargetTempHI"
    var topicTargetTempLO = prefixTopic + "/" + deviceName + "/Edge/TargetTempLO"
    var topicFanMode= prefixTopic + "/" + deviceName + "/Edge/fanMode"
    var topicHvacAction = prefixTopic + "/" + deviceName + "/Edge/hvacAction"
    var topicPresetMode = prefixTopic + "/" + deviceName + "/Edge/presetMode"
    var topicAuxHeat = prefixTopic + "/" + deviceName + "/Edge/auxHeat"
    var topicFan = prefixTopic + "/" + deviceName + "/Edge/fanAction"
    var topicClimateMode = prefixTopic + "/" + deviceName + "/Edge/climateMode"
    var topicEquipmentRunning = prefixTopic + "/" + deviceName + "/Edge/equipmentRunning"
    var topicFanMinOnTime= prefixTopic + "/" + deviceName + "/Edge/fanMinOnTime"

    var msgHvacMode = {
        payload: msg.payload.state,
        topic: topicHvacMode,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };
    
    var msgMinTemp = {
        payload: msg.payload.attributes.min_temp,
        topic: topicMinTemp,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };
    
    var msgMaxTemp = {
        payload: msg.payload.attributes.max_temp,
        topic: topicMaxTemp,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };
    
    var msgTargetTempHI = {
        payload: msg.payload.attributes.target_temp_high,
        topic: topicTargetTempHI,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };
    
    var msgTargetTempLO = {
        payload: msg.payload.attributes.target_temp_low,
        topic: topicTargetTempLO,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };

    var msgFanMode = {
        payload: msg.payload.attributes.fan_mode,
        topic: topicFanMode,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };

    var msgHvacAction = {
        payload: msg.payload.attributes.hvac_action,
        topic: topicHvacAction,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };

    var msgPresetMode = {
        payload: msg.payload.attributes.preset_mode,
        topic: topicPresetMode,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };

    var msgAuxHeat = {
        payload: msg.payload.attributes.aux_heat,
        topic: topicAuxHeat,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };

    var msgFan = {
        payload: msg.payload.attributes.fan,
        topic: topicFan,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };

    var msgClimateMode = {
        payload: msg.payload.attributes.climate_mode,
        topic: topicClimateMode,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };

    var msgEquipmentRunning = {
        payload: msg.payload.attributes.equipment_running,
        topic: topicEquipmentRunning,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };

    var msgFanMinOnTime = {
        payload: msg.payload.attributes.fan_min_on_time,
        topic: topicFanMinOnTime,
        qos: mqttQosMode,
        retain: mqttRetainMode
    };

}
                
return [msgHvacMode,msgMinTemp,msgMaxTemp,msgTargetTempHI,msgTargetTempLO,msgFanMode,msgHvacAction,msgPresetMode,msgAuxHeat,msgFan,msgClimateMode,msgEquipmentRunning, msgFanMinOnTime];