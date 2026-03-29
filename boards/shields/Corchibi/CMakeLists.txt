# zephyr_library()


#---
# Patch 1: Skip CONFIGURATION_RESET on startup (causes I2C issues on nRF52840)
# Patch 2: Add movement threshold filter (like PMW3610's MOVEMENT_THRESHOLD)
#          Prevents micro-movements from reaching ZMK's input subsystem,
#          allowing idle timer to work correctly.
#---
set(FILE_PATH "${ZEPHYR_BASE}/drivers/input/input_pat912x.c")
file(READ "${FILE_PATH}" FILE_CONTENT)

# Patch 1: Skip CONFIGURATION_RESET write
string(
  REPLACE "\ti2c_reg_write_byte_dt(&cfg->i2c, PAT912X_CONFIGURATION, CONFIGURATION_RESET);\n"
          "\t\/\/ i2c_reg_write_byte_dt(&cfg->i2c, PAT912X_CONFIGURATION, CONFIGURATION_RESET);\n"
  FILE_CONTENT "${FILE_CONTENT}"
)

# Patch 2: Add movement threshold filter before input_report_rel()
# Only report motion if abs(x)+abs(y) > 5 (same threshold as PMW3610)
string(
  REPLACE "\tLOG_DBG(\"x=%4d y=%4d\", x, y);\n\n\tif (cfg->axis_x >= 0) {"
          "\tLOG_DBG(\"x=%4d y=%4d\", x, y);\n\n\t\/\/ Movement threshold filter (like PMW3610 MOVEMENT_THRESHOLD=5)\n\tif (abs(x) + abs(y) <= 15) {\n\t\tk_work_submit(&data->motion_work);\n\t\treturn;\n\t}\n\n\tif (cfg->axis_x >= 0) {"
  FILE_CONTENT "${FILE_CONTENT}"
)

file(WRITE "${FILE_PATH}" "${FILE_CONTENT}")
message(STATUS "Patched PAT912x driver (reset skip + movement threshold): ${FILE_PATH}")


# zephyr_include_directories(include)
