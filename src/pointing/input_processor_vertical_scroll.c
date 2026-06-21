/*
 * Copyright (c) 2026
 *
 * SPDX-License-Identifier: MIT
 */

#define DT_DRV_COMPAT zmk_input_processor_vertical_scroll

#include <stdlib.h>

#include <zephyr/device.h>
#include <zephyr/dt-bindings/input/input-event-codes.h>
#include <zephyr/input/input.h>
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/util.h>

#include <drivers/input_processor.h>
#include <dt-bindings/zmk/modifiers.h>
#include <zmk/hid.h>

LOG_MODULE_DECLARE(zmk, CONFIG_ZMK_LOG_LEVEL);

struct vertical_scroll_config {
    uint8_t type;
};

static bool shift_is_pressed(void) {
    return (zmk_hid_get_explicit_mods() & (MOD_LSFT | MOD_RSFT)) != 0;
}

static int vertical_scroll_handle_event(const struct device *dev, struct input_event *event,
                                        uint32_t param1, uint32_t param2,
                                        struct zmk_input_processor_state *state) {
    const struct vertical_scroll_config *cfg = dev->config;

    if (event->type != cfg->type) {
        return ZMK_INPUT_PROC_CONTINUE;
    }

    switch (event->code) {
    case INPUT_REL_X:
    case INPUT_REL_Y:
        event->code = shift_is_pressed() ? INPUT_REL_HWHEEL : INPUT_REL_WHEEL;
        event->sync = true;
        break;
    default:
        return ZMK_INPUT_PROC_CONTINUE;
    }

    if (event->value == 0) {
        return ZMK_INPUT_PROC_STOP;
    }

    LOG_DBG("scroll %s=%d", event->code == INPUT_REL_HWHEEL ? "hwheel" : "wheel",
            event->value);

    return ZMK_INPUT_PROC_CONTINUE;
}

static struct zmk_input_processor_driver_api vertical_scroll_driver_api = {
    .handle_event = vertical_scroll_handle_event,
};

#define VERTICAL_SCROLL_INST(n)                                                                    \
    static const struct vertical_scroll_config vertical_scroll_config_##n = {                      \
        .type = DT_INST_PROP_OR(n, type, INPUT_EV_REL),                                            \
    };                                                                                             \
    DEVICE_DT_INST_DEFINE(n, NULL, NULL, NULL, &vertical_scroll_config_##n, POST_KERNEL,           \
                          CONFIG_KERNEL_INIT_PRIORITY_DEFAULT, &vertical_scroll_driver_api);

DT_INST_FOREACH_STATUS_OKAY(VERTICAL_SCROLL_INST)
