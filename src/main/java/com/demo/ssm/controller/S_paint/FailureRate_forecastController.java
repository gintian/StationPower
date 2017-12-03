package com.demo.ssm.controller.S_paint;

import com.alibaba.fastjson.JSONObject;
import com.demo.ssm.po.S_paint.FailureRate_forecast;
import com.demo.ssm.service.interf.S_paint.FailureRate_forecastService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;

@Controller
@RequestMapping("/FailureRate_forecast")
public class FailureRate_forecastController {
    @Autowired
    private FailureRate_forecastService failureRate_forecastService;
    //查询异常对象数据
    @RequestMapping("/select")
    @ResponseBody
    public JSONObject S_dataQuality(HttpServletRequest request,String Province,String id){
//        JSONArray jsonArray=new JSONArray();
        JSONObject jsonObject = new JSONObject();
        String time=null;
        double eta=0;
        double beta=0;
        try {

                FailureRate_forecast equi = failureRate_forecastService.Query(id,Province);
                if(equi==null){
                    jsonObject.put("result",false);
                }else {
                    time = equi.getALARM_TIME_D();
                    beta = equi.getBETA();
                    eta = equi.getETA();
                    jsonObject.put("time", time);
                    jsonObject.put("beta", beta);
                    jsonObject.put("eta", eta);
                }
                return jsonObject;
//            System.out.println("result:"+ JSON.toJSONString(jsonArray));

//            return jsonArray;

        } catch (IOException e) {
            e.printStackTrace();
            jsonObject.put("result",false);
//            jsonArray.add(jsonObject);
            return jsonObject;

        }

    }






    /*public ModelAndView S_dataQuality()throws Exception{
        //调用servic查找数据库
        Abnormal_top10 abnormal_top10 = abnormal_top10Service.selectByPrimaryKey(null);

        ModelAndView modelAndView = new ModelAndView();

        modelAndView.addObject("abnormal_top10",abnormal_top10);

        modelAndView.setViewName("S_dataQuality");

        return modelAndView;

    }*/


}
