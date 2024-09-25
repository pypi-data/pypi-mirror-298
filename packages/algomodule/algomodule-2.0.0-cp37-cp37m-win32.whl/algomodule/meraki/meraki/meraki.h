/* meraki: C/C++ implementation of Meraki, the Telestai Proof of Work algorithm.
 * Copyright 2018-2019 Pawel Bylica.
 * Licensed under the Apache License, Version 2.0.
 */

#pragma once

#include "algomodule/meraki/support/hash_types.h"

#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * The Meraki algorithm revision implemented as specified in the Meraki spec
 * https://github.com/ethereum/wiki/wiki/Meraki.
 */
#define MERAKI_REVISION "23"

#define MERAKI_EPOCH_LENGTH 27500
#define MERAKI_LIGHT_CACHE_ITEM_SIZE 64
#define MERAKI_FULL_DATASET_ITEM_SIZE 128
#define MERAKI_NUM_DATASET_ACCESSES 32


struct meraki_epoch_context
{
    const int epoch_number;
    const int light_cache_num_items;
    const union meraki_hash512* const light_cache;
    const uint32_t* const l1_cache;
    const int full_dataset_num_items;
};


struct meraki_epoch_context_full;


struct meraki_result
{
    union meraki_hash256 final_hash;
    union meraki_hash256 mix_hash;
};


/**
 * Calculates the number of items in the light cache for given epoch.
 *
 * This function will search for a prime number matching the criteria given
 * by the Meraki so the execution time is not constant. It takes ~ 0.01 ms.
 *
 * @param epoch_number  The epoch number.
 * @return              The number items in the light cache.
 */
int meraki_calculate_light_cache_num_items(int epoch_number) ;


/**
 * Calculates the number of items in the full dataset for given epoch.
 *
 * This function will search for a prime number matching the criteria given
 * by the Meraki so the execution time is not constant. It takes ~ 0.05 ms.
 *
 * @param epoch_number  The epoch number.
 * @return              The number items in the full dataset.
 */
int meraki_calculate_full_dataset_num_items(int epoch_number) ;

/**
 * Calculates the epoch seed hash.
 * @param epoch_number  The epoch number.
 * @return              The epoch seed hash.
 */
union meraki_hash256 meraki_calculate_epoch_seed(int epoch_number) ;


struct meraki_epoch_context* meraki_create_epoch_context(int epoch_number) ;

/**
 * Creates the epoch context with the full dataset initialized.
 *
 * The memory for the full dataset is only allocated and marked as "not-generated".
 * The items of the full dataset are generated on the fly when hit for the first time.
 *
 * The memory allocated in the context MUST be freed with meraki_destroy_epoch_context_full().
 *
 * @param epoch_number  The epoch number.
 * @return  Pointer to the context or null in case of memory allocation failure.
 */
struct meraki_epoch_context_full* meraki_create_epoch_context_full(int epoch_number) ;

void meraki_destroy_epoch_context(struct meraki_epoch_context* context) ;

void meraki_destroy_epoch_context_full(struct meraki_epoch_context_full* context) ;


/**
 * Get global shared epoch context.
 */
const struct meraki_epoch_context* meraki_get_global_epoch_context(int epoch_number) ;

/**
 * Get global shared epoch context with full dataset initialized.
 */
const struct meraki_epoch_context_full* meraki_get_global_epoch_context_full(
    int epoch_number) ;


struct meraki_result meraki_hash(const struct meraki_epoch_context* context,
    const union meraki_hash256* header_hash, uint64_t nonce) ;

bool meraki_verify(const struct meraki_epoch_context* context,
    const union meraki_hash256* header_hash, const union meraki_hash256* mix_hash, uint64_t nonce,
    const union meraki_hash256* boundary) ;

bool meraki_verify_final_hash(const union meraki_hash256* header_hash,
    const union meraki_hash256* mix_hash, uint64_t nonce,
    const union meraki_hash256* boundary) ;

union meraki_hash256 light_verify(const union meraki_hash256* header_hash,
                       const union meraki_hash256* mix_hash, uint64_t nonce) ;

#ifdef __cplusplus
}
#endif
