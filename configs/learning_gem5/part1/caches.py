# -*- coding: utf-8 -*-
# Copyright (c) 2015 Jason Power
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

""" Caches with options for a simple gem5 configuration script

This file contains L1 I/D and L2 caches to be used in the simple
gem5 configuration script. It uses the SimpleOpts wrapper to set up command
line options from each individual class.
"""

import m5
from m5.objects import Cache, WriteAllocator
from m5.params import Param

from m5.objects.ReplacementPolicies import *
import m5.objects.ReplacementPolicies

# Add the common scripts to our path
m5.util.addToPath("../../")
import importlib
from common import SimpleOpts

# Some specific options for caches
# For all options see src/mem/cache/BaseCache.py

# Create a dictionary that maps replacement policy names to their classes
replacement_policies_l1i = {
    "LRU": LRURP(),
    "Random": RandomRP(),
    "FIFO": FIFORP(),
    # Add more replacement policies here...
}

# Create a dictionary that maps replacement policy names to their classes
replacement_policies_l1d = {
    "LRU": LRURP(),
    "Random": RandomRP(),
    "FIFO": FIFORP(),
    # Add more replacement policies here...
}

# Create a dictionary that maps replacement policy names to their classes
replacement_policies_l2 = {
    "LRU": LRURP(),
    "Random": RandomRP(),
    "FIFO": FIFORP(),
    # Add more replacement policies here...
}


class L1Cache(Cache):
    """Simple L1 Cache with default values"""

    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    write_allocator = WriteAllocator()

    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass

    def connectBus(self, bus):
        """Connect this cache to a memory-side bus"""
        self.mem_side = bus.cpu_side_ports

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU-side port
        This must be defined in a subclass"""
        raise NotImplementedError


class L1ICache(L1Cache):
    """Simple L1 instruction cache with default values"""

    # Set the default size
    size = "16kB"
    assoc = 2
    replacement_policy = LRURP()

    SimpleOpts.add_option(
        "--l1i_size", help=f"L1 instruction cache size. Default: {size}"
    )
    SimpleOpts.add_option(
        "--l1i_assoc", help=f"L1 instruction cache assoc. Default: {assoc}"
    )
    SimpleOpts.add_option(
        "--l1i_rp", help=f"L1 instruction cache replacement policy. Default: {replacement_policy}"
    )

    def __init__(self, opts=None):
        super(L1ICache, self).__init__(opts)
        if opts:
            if opts.l1i_size:
                self.size = opts.l1i_size
            if opts.l1i_assoc:
                self.assoc = opts.l1i_assoc
            if opts.l1i_rp:
                self.replacement_policy = replacement_policies_l1i[opts.l1i_rp]

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU icache port"""
        self.cpu_side = cpu.icache_port


class L1DCache(L1Cache):
    """Simple L1 data cache with default values"""

    # Set the default size
    size = "64kB"
    assoc = 2
    replacement_policy = LRURP()

    SimpleOpts.add_option(
        "--l1d_size", help=f"L1 data cache size. Default: {size}"
    )
    SimpleOpts.add_option(
        "--l1d_assoc", help=f"L1 data cache assoc. Default: {assoc}"
    )
    SimpleOpts.add_option(
        "--l1d_rp", help=f"L1 data cache replacement policy. Default: {replacement_policy}"
    )


    def __init__(self, opts=None):
        super(L1DCache, self).__init__(opts)
        if opts:
            if opts.l1d_size:
                self.size = opts.l1d_size
            if opts.l1d_assoc:
                self.assoc = opts.l1d_assoc
            if opts.l1d_rp:
                self.replacement_policy = replacement_policies_l1d[opts.l1d_rp]

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU dcache port"""
        self.cpu_side = cpu.dcache_port


class L2Cache(Cache):
    """Simple L2 Cache with default values"""

    # Default parameters
    size = "256kB"
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
    replacement_policy = LRURP()
    SimpleOpts.add_option("--l2_size", help=f"L2 cache size. Default: {size}")
    SimpleOpts.add_option(
        "--l2_assoc", help=f"L2 cache assoc. Default: {assoc}"
    )
    SimpleOpts.add_option(
        "--l2_rp", help=f"L2 cache replacement policy. Default: {replacement_policy}"
    )

    def __init__(self, opts=None):
        super(L2Cache, self).__init__()
        if opts:
            if opts.l2_size:
                self.size = opts.l2_size
            if opts.l2_assoc:
                self.assoc = opts.l2_assoc
            if opts.l2_rp:
                self.replacement_policy = replacement_policies_l2[opts.l2_rp]


    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports
