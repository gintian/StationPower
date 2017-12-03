package com.demo.ssm.service.Impl.S_data;

import com.demo.ssm.mapper.S_data.Accurate_top10Mapper;
import com.demo.ssm.po.S_data.Accurate_top10;
import com.demo.ssm.service.interf.S_data.Accurate_top10Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;

@Service
public class Accurate_top10ServiceImpl implements Accurate_top10Service {

    @Autowired
    private Accurate_top10Mapper accurate_top10Mapper;

    @Override
    public List<Accurate_top10> selectByPrimaryKey() throws IOException{

        return accurate_top10Mapper.selectByPrimaryKey();


    }

    @Override
    public  int count() throws IOException{
        return accurate_top10Mapper.count();
    }


}
