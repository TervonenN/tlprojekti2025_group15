/*
 * Copyright (c) 2020 Libre Solar Technologies GmbH
 *
 * SPDX-License-Identifier: Apache-2.0
 */
#include <zephyr/logging/log.h>
#include <dk_buttons_and_leds.h>
#include <inttypes.h>
#include <stddef.h>
#include <stdint.h>
#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/util.h>
#include "adc.h"
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/gap.h>
#include <zephyr/bluetooth/uuid.h>
#include <zephyr/bluetooth/conn.h>
#include "my_lbs.h"

#define USER_LED1         	 	DK_LED1
#define USER_LED2          		DK_LED2
#define USER_LED3               DK_LED3
#define USER_LED4               DK_LED4

#define USER_BUTTON_1           DK_BTN1_MSK
#define USER_BUTTON_2           DK_BTN2_MSK
#define USER_BUTTON_3           DK_BTN3_MSK
#define USER_BUTTON_4           DK_BTN4_MSK

LOG_MODULE_REGISTER(MAIN, LOG_LEVEL_INF);

static uint8_t direction = 0; // Globaali muuttuja suunnalle

// BLE advertising data
static const struct bt_data ad[] = {
	BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
	BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME, sizeof(CONFIG_BT_DEVICE_NAME) - 1),
};

static void button_changed(uint32_t button_state, uint32_t has_changed)
{
	if ((has_changed & USER_BUTTON_1) && (button_state & USER_BUTTON_1)) 
	{
		printk("Nappi 1 alhaalla\n");
	}

	if ((has_changed & USER_BUTTON_2) && (button_state & USER_BUTTON_2)) 
	{
		direction = (direction + 1) % 6; // 0→1→2→3→4→5→0
		printk("Suunta vaihdettu: %d\n", direction);
	}		
	
	if ((has_changed & USER_BUTTON_3) && (button_state & USER_BUTTON_3)) 
	{
		printk("Nappi 3 alhaalla\n");
	}		

	if ((has_changed & USER_BUTTON_4) && (button_state & USER_BUTTON_4)) 
	{
		printk("Nappi 4 alhaalla\n");
	}		
}

int main(void)
{
	int err;
	
	// LEDit ja napit
	err = dk_leds_init();
	if (err) {
		LOG_ERR("LEDs init failed (err %d)\n", err);
		return -1;
	}

	err = dk_buttons_init(button_changed);
	if (err) {
		printk("Cannot init buttons (err: %d)\n", err);
		return -1;
	}
	
	// ADC init
	if(initializeADC() != 0)
	{
		printk("ADC initialization failed!");
		return -1;
	}

	// ***** LISÄÄ BLE INIT TÄHÄN *****
	err = bt_enable(NULL);
	if (err) {
		printk("Bluetooth init failed (err %d)\n", err);
		return -1;
	}
	printk("Bluetooth initialized\n");

	err = my_lbs_init(NULL);
	if (err) {
		printk("Failed to init LBS (err:%d)\n", err);
		return -1;
	}

	err = bt_le_adv_start(BT_LE_ADV_CONN, ad, ARRAY_SIZE(ad), NULL, 0);
	if (err) {
		printk("Advertising failed to start (err %d)\n", err);
		return -1;
	}
	printk("Advertising successfully started\n");
	// ***** BLE INIT LOPPUU *****

	while (1) 
	{
		struct Measurement m = readADCValue();
		printk("Suunta=%d, x=%d, y=%d, z=%d\n", direction, m.x, m.y, m.z);
		
		// ***** LÄHETÄ BLE:n yli *****
		my_lbs_send_sensor_notify(direction);
		k_sleep(K_MSEC(100));
		my_lbs_send_sensor_notify(m.x);
		k_sleep(K_MSEC(100));
		my_lbs_send_sensor_notify(m.y);
		k_sleep(K_MSEC(100));
		my_lbs_send_sensor_notify(m.z);
		// ***** LÄHETYS LOPPUU *****
		
		k_sleep(K_MSEC(1000));
		
		dk_set_led_on(USER_LED1);
		dk_set_led_on(USER_LED2);
		dk_set_led_on(USER_LED3);
		dk_set_led_on(USER_LED4);
		 
		k_sleep(K_MSEC(1000));
		
		dk_set_led_off(USER_LED1);
		dk_set_led_off(USER_LED2);
		dk_set_led_off(USER_LED3);
		dk_set_led_off(USER_LED4);
	}
	
	return 0;
}