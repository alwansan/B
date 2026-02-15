cmake_minimum_required(VERSION 3.18.0)

project("bootstrap")

# إنشاء مكتبة مشتركة (Shared Library)
add_library(
        bootstrap
        SHARED
        bootstrap.c)

# ربط مكتبات النظام (Log)
find_library(
        log-lib
        log)

target_link_libraries(
        bootstrap
        ${log-lib})