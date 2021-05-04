/* Routines for using cycle counter */
#pragma once

/* Start the counter */
void start_counter();

/* Get # cycles since counter started */
double get_counter();

/* Determine clock rate of processor (using a default sleeptime) */
double mhz(int verbose);

/* Determine clock rate of processor, having more control over accuracy */
double mhz_full(int verbose, int sleeptime);

/* Special counters that compensate for timer interrupt overhead */
void start_comp_counter();
double get_comp_counter();
