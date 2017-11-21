package com.demo.ssm.mapper;

import com.demo.ssm.po.Relationship_Temperature_FailureRate;
import org.springframework.stereotype.Repository;

import java.io.IOException;
import java.util.List;

@Repository
public interface Relationship_Temperature_FailureRateMapper {
    List<Relationship_Temperature_FailureRate> selectByPrimaryKey() throws IOException;

    int count() throws IOException;
}
