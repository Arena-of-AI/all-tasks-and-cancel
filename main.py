import streamlit as st
import openai
from datetime import datetime

# 设置OpenAI API密钥的输入框
api_key = st.text_input("Enter your OpenAI API key")

# 如果API密钥已提供，则进行身份验证
if api_key:
    openai.api_key = api_key
else:
    st.warning("Please enter your OpenAI API key.")

# 处理"List all jobs"按钮的点击事件
if st.button("List all jobs"):
    # 调用OpenAI FineTune.list()获取所有作业的信息
    response = openai.FineTune.list()

    # 解析并显示作业信息的简化表格
    jobs_data = response["data"]
    table_data = []
    for job in jobs_data:
        created_at = job["created_at"]
        fine_tuned_model = job["fine_tuned_model"]
        model = job["model"]
        status = job["status"]

        # 将UNIX时间戳转换为可读日期时间格式
        created_at_formatted = datetime.fromtimestamp(created_at).strftime("%Y-%m-%d %H:%M:%S")

        table_data.append([created_at_formatted, fine_tuned_model, model, status])

    st.table(table_data, columns=["Created at", "Fine-Tuned Model", "Model", "Status"])


# 处理"Cancel job"按钮的点击事件
cancel_job_id = st.text_input("Enter the job ID to cancel")
if st.button("Cancel job") and cancel_job_id:
    # 调用OpenAI FineTune.cancel()取消指定的作业
    response = openai.FineTune.cancel(id=cancel_job_id)

    # 检查作业的状态以确定是否成功取消
    status = response.get("status")
    if status == "cancelled":
        st.success("The job is successfully canceled")
    else:
        st.error("Failed to cancel the job")
