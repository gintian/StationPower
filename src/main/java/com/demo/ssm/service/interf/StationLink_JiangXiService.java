package com.demo.ssm.service.interf;

import com.demo.ssm.po.Abnormal_top10;
import com.demo.ssm.po.StationLink_JiangXi;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;

@Service
public interface StationLink_JiangXiService {

    List<StationLink_JiangXi> selectByPrimaryKey() throws IOException;

    int count() throws IOException;
}
