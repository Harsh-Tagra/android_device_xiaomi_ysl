#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/qcom-caf/msm8996',
    'hardware/xiaomi',
    'vendor/xiaomi/msm8953-common',
]

blob_fixups: blob_fixups_user_type = {
    ('vendor/lib/libarcsoft_high_dynamic_range.so', 'vendor/lib/libremosaic_wrapper.so', 'vendor/lib/libremosaiclib.so', 'vendor/lib/libmmcamera_hdr_gb_lib.so'): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib/libgf_hal.so': blob_fixup()
        .sig_replace('00 c6 8f e2 4a ca 8c e2 b0 fa bc e5', '00 c6 8f e2 1f 20 03 d5 b0 fa bc e5')
        .sig_replace('78 47 c0 46 00 c0 9f e5 0f f0 8c e0 e0 37 fc ff', '78 47 c0 46 1f 20 03 d5 0f f0 8c e0 e0 37 fc ff'),
    'vendor/lib/libvendor.goodix.hardware.fingerprint@1.0-service.so': blob_fixup()
        .remove_needed('libprotobuf-cpp-lite.so')
        .binary_regex_replace(b'libvendor.goodix.hardware.fingerprint@1.0.so', b'vendor.goodix.hardware.fingerprint@1.0.so\x00\x00\x00'),
    'vendor/lib64/hw/consumerir.msm8953.so': blob_fixup()
        .binary_regex_replace(b'/dev/spidev6.1', b'/dev/spidev5.1')
}  # fmt: skip

module = ExtractUtilsModule(
    'ysl',
    'xiaomi',
    blob_fixups=blob_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'msm8953-common', module.vendor
    )
    utils.run()
