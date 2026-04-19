#include <WiFi.h>
#include <esp_wifi.h>
#include <esp_coexist.h>
#include <BLEDevice.h>
#include <BLEScan.h>
#include <map>

#define WIFI_CHANNEL 1

BLEScan* pBLEScan;
std::map<String, unsigned long> lastSeen;

wifi_promiscuous_filter_t filt = {
  .filter_mask = WIFI_PROMIS_FILTER_MASK_MGMT
};

// WiFi Sniffer Callback
void wifi_sniffer(void* buf, wifi_promiscuous_pkt_type_t type) {
  if (type != WIFI_PKT_MGMT) return;

  wifi_promiscuous_pkt_t *pkt = (wifi_promiscuous_pkt_t*)buf; //  fixed
  int rssi = pkt->rx_ctrl.rssi;
  uint8_t *payload = pkt->payload;

  uint8_t frame_type = payload[0];
  if ((frame_type & 0xF0) != 0x40) return;

  char mac[18];
  sprintf(mac, "%02X:%02X:%02X:%02X:%02X:%02X",
    payload[10], payload[11], payload[12],
    payload[13], payload[14], payload[15]);

  String macStr = String(mac);
  if (millis() - lastSeen[macStr] < 2000) return;
  lastSeen[macStr] = millis();

  Serial.print("WIFI,");
  Serial.print(macStr);
  Serial.print(",");
  Serial.print(rssi);
  Serial.print(",");
  Serial.println(millis());
}

// BLE Callback
class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice advertisedDevice) {
    String mac = advertisedDevice.getAddress().toString().c_str();
    if (millis() - lastSeen[mac] < 2000) return;
    lastSeen[mac] = millis();

    Serial.print("BLE,");
    Serial.print(mac);
    Serial.print(",");
    Serial.print(advertisedDevice.getRSSI());
    Serial.print(",");
    Serial.println(millis());
  }
};

void setup() {
  Serial.begin(115200);

  esp_coex_preference_set(ESP_COEX_PREFER_BALANCE); // ✅ WiFi+BLE coexistence

  WiFi.mode(WIFI_STA);
  esp_wifi_start();
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_promiscuous_filter(&filt);
  esp_wifi_set_promiscuous_rx_cb(&wifi_sniffer);
  esp_wifi_set_channel(WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);

  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);

  Serial.println("TYPE,MAC,RSSI,TIMESTAMP");
  Serial.println("READY");
}

void loop() {
  pBLEScan->start(2, false);
  pBLEScan->clearResults(); // free memory after each scan

  //  prevent memory leak
  if (lastSeen.size() > 200) {
    lastSeen.clear();
  }
}