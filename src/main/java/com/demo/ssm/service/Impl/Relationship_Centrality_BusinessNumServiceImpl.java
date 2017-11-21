package com.demo.ssm.service.Impl;

import com.demo.ssm.mapper.Relationship_Centrality_BusinessNumMapper;
import com.demo.ssm.po.Relationship_Centrality_BusinessNum;
import com.demo.ssm.service.interf.Relationship_Centrality_BusinessNumService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;

@Service
public class Relationship_Centrality_BusinessNumServiceImpl implements Relationship_Centrality_BusinessNumService {

    @Autowired
    private Relationship_Centrality_BusinessNumMapper relationship_Centrality_BusinessNumMapper;

    @Override
    public List<Relationship_Centrality_BusinessNum> selectByPrimaryKey() throws IOException{

        return relationship_Centrality_BusinessNumMapper.selectByPrimaryKey();


    }

    @Override
    public  int count() throws IOException{
        return relationship_Centrality_BusinessNumMapper.count();
    }


}
