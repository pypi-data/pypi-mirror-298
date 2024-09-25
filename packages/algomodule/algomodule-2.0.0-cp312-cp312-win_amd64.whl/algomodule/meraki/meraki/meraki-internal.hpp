// meraki: C/C++ implementation of Meraki, the Telestai Proof of Work algorithm.
// Copyright 2018-2019 Pawel Bylica.
// Licensed under the Apache License, Version 2.0.

/// @file
/// Contains declarations of internal meraki functions to allow them to be
/// unit-tested.

#pragma once

#include "algomodule/meraki/meraki/meraki.hpp"

#include "endianness.hpp"

#include <memory>
#include <vector>

extern "C" struct meraki_epoch_context_full : meraki_epoch_context
{
    meraki_hash1024* full_dataset;

    constexpr meraki_epoch_context_full(int epoch, int light_num_items,
        const meraki_hash512* light, const uint32_t* l1, int dataset_num_items,
        meraki_hash1024* dataset) 
      : meraki_epoch_context{epoch, light_num_items, light, l1, dataset_num_items},
        full_dataset{dataset}
    {}
};

namespace meraki
{
inline bool is_less_or_equal(const hash256& a, const hash256& b) 
{
    for (size_t i = 0; i < (sizeof(a) / sizeof(a.word64s[0])); ++i)
    {
        if (be::uint64(a.word64s[i]) > be::uint64(b.word64s[i]))
            return false;
        if (be::uint64(a.word64s[i]) < be::uint64(b.word64s[i]))
            return true;
    }
    return true;
}

inline bool is_equal(const hash256& a, const hash256& b) 
{
    return std::memcmp(a.bytes, b.bytes, sizeof(a)) == 0;
}

void build_light_cache(hash512 cache[], int num_items, const hash256& seed) ;

hash512 calculate_dataset_item_512(const epoch_context& context, int64_t index) ;
hash1024 calculate_dataset_item_1024(const epoch_context& context, uint32_t index) ;
hash2048 calculate_dataset_item_2048(const epoch_context& context, uint32_t index) ;

namespace generic
{
using hash_fn_512 = hash512 (*)(const uint8_t* data, size_t size);
using build_light_cache_fn = void (*)(hash512 cache[], int num_items, const hash256& seed);

void build_light_cache(
    hash_fn_512 hash_fn, hash512 cache[], int num_items, const hash256& seed) ;

epoch_context_full* create_epoch_context(
    build_light_cache_fn build_fn, int epoch_number, bool full) ;

}  // namespace generic

}  // namespace meraki
