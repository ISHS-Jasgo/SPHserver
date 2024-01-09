package com.github.jasgo

import com.aparapi.Kernel

fun main() {
    try {
        val inputA = doubleArrayOf(1.0, 2.0, 3.0)
        val inputB = doubleArrayOf(4.0, 5.0, 6.0)

        val result = DoubleArray(inputA.size)

        val kernel = object : Kernel() {
            override fun run() {
                val i = globalId
                result[i] = inputA[i] + inputB[i]
            }
        }
        kernel.setExecutionModeWithoutFallback(Kernel.EXECUTION_MODE.GPU)
        kernel.execute(inputA.size)
        for (i in result.indices) {
            println("${inputA[i]} + ${inputB[i]} = ${result[i]}")
        }
        kernel.dispose()
    } catch (ignored: Exception) { }
}