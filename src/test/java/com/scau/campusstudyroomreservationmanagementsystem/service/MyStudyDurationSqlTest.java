package com.scau.campusstudyroomreservationmanagementsystem.service;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * 防止 myStudyDuration 年报 SQL 中 date_format 占位符被 String.formatted 误解析。
 */
class MyStudyDurationSqlTest {

    @Test
    void yearAggregationSqlShouldPreserveMysqlDateFormat() {
        String minutesExpr = "greatest(0, timestampdiff(minute, reservation.sign_in_time, reservation.sign_out_time))";
        String predicate = "reservation.status in ('已完成','使用中')";
        String sql = """
                select date_format(reserve_date,'%%Y-%%m') label, sum(%s) minutes
                from reservation
                where user_id=? and %s
                  and reserve_date >= date_sub(current_date(), interval 365 day)
                group by date_format(reserve_date,'%%Y-%%m')
                order by label
                """.formatted(minutesExpr, predicate);

        assertTrue(sql.contains("date_format(reserve_date,'%Y-%m')"));
        assertFalse(sql.contains("%%Y"));
    }
}
