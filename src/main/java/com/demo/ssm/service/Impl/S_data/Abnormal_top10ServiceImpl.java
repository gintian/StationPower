package com.demo.ssm.service.Impl.S_data;

import com.demo.ssm.mapper.S_data.Abnormal_top10Mapper;
import com.demo.ssm.po.S_data.Abnormal_top10;
import com.demo.ssm.service.interf.S_data.Abnormal_top10Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;

@Service
public class Abnormal_top10ServiceImpl implements Abnormal_top10Service {

    @Autowired
    private Abnormal_top10Mapper abnormal_top10Mapper;

    @Override
    public List<Abnormal_top10> selectByPrimaryKey() throws IOException{

        return abnormal_top10Mapper.selectByPrimaryKey();


    }

    @Override
    public  int count() throws IOException{
        return abnormal_top10Mapper.count();
    }


}
