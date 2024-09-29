def tpeAI(values, language="English", base_url="http://20.240.210.52:1688/v1/",
            api_key="sk-Qjeu6nlITz74zmsP92Cf6c53C89b44B3A0232c0f15564021"):
    import pandas as pd
    from openai import OpenAI
    prompt_Chinese=f"""
         As a respiratory disease expert specializing in the diagnosis and treatment of tuberculous pleural effusion, please analyze the data from the first part related to laboratory tests and clinical features of tuberculous pleural effusion that I uploaded. In this data, the GROUP column indicates 0 for non-tuberculous pleural effusion and 1 for tuberculous pleural effusion. If you can recognize this, please respond with "yes" and make a prediction about whether the data in the second part is indicative of tuberculous pleural effusion. Here is the data from the first part::"
GROUP	Pleural fluid biochemistry_ADA	Pleural fluid biochemistry_Total protein	Blood cell analysis_Lymphocyte count	Pleural fluid biochemistry_Albumin	Blood cell analysis_Neutrophil percentage	Blood cell analysis_Monocyte percentage	Blood cell analysis_Neutrophil count	Age
0	0	1	1	1	0	1	0	1
1	1	1	0	1	0	1	0	1
0	1	1	1	1	1	0	1	1
0	0	0	0	0	0	0	1	1
1	0	0	1	1	0	0	0	0
1	1	0	0	1	0	1	0	1
1	1	1	0	1	0	1	0	1
0	0	0	0	1	1	0	1	1
1	1	0	0	1	0	1	0	1
1	1	1	0	1	0	1	0	0
1	1	1	0	1	0	1	0	0
1	1	1	0	1	0	1	0	0
0	0	1	0	1	0	1	0	1
1	1	1	1	1	0	0	1	0
1	1	1	0	1	1	1	1	1
1	0	0	0	0	1	1	1	1
1	1	1	0	0	0	1	0	1
0	0	0	0	0	0	1	0	1
0	0	1	1	1	0	0	1	1
0	0	0	0	0	1	0	1	1
0	0	1	1	1	0	0	1	1
1	1	1	0	1	0	1	0	0
0	1	0	0	0	0	1	1	1
1	1	1	1	1	0	1	1	1
0	0	0	1	0	0	1	1	1
1	1	0	0	0	0	0	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	1	0	1	0	1
0	0	1	1	1	0	0	1	1
1	1	1	0	1	0	1	0	1
1	0	1	0	1	0	1	1	1
0	0	1	1	1	0	1	1	1
1	1	0	1	1	0	1	0	1
0	0	1	0	1	1	0	0	1
0	1	1	0	0	0	0	0	1
1	1	1	1	1	0	1	1	1
0	0	0	0	1	0	1	1	1
1	1	1	1	1	0	1	0	0
0	0	0	1	1	0	1	0	1
0	1	0	1	1	0	1	1	1
0	0	0	1	0	1	1	1	1
1	1	1	0	1	0	1	0	0
1	1	1	1	1	0	0	0	1
1	1	1	0	1	0	1	0	0
1	1	1	0	0	0	1	0	1
1	1	1	0	1	0	1	0	1
0	0	1	1	1	0	1	0	1
1	1	1	0	1	0	1	0	0
0	0	0	1	1	0	1	1	1
1	1	1	1	1	0	0	1	1
1	1	1	0	1	1	1	1	0
0	0	0	1	1	0	1	1	1
0	0	1	0	1	1	0	1	0
1	1	1	0	0	0	1	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	1	0	1	1	1
1	0	1	1	1	0	1	0	1
1	0	0	0	1	0	1	0	1
1	0	1	1	1	0	1	1	1
1	1	0	0	1	0	1	0	1
1	1	1	0	1	0	1	0	0
0	0	1	1	1	0	1	1	1
1	1	1	0	1	0	1	0	0
1	0	0	0	0	0	1	0	1
0	1	0	0	0	1	1	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	1	1	0	1	1
1	1	1	0	1	0	1	0	1
1	1	0	0	0	0	1	1	1
1	1	0	0	1	1	0	1	1
1	1	0	0	0	0	1	0	1
1	1	0	0	1	0	1	0	0
0	1	1	0	0	1	0	1	1
1	1	1	0	1	0	1	0	1
1	0	0	0	0	0	1	0	1
0	0	0	1	1	0	0	0	1
1	1	0	0	1	0	1	0	1
0	0	0	1	1	0	0	0	1
1	1	1	0	1	0	1	0	1
0	0	0	0	1	0	0	0	1
0	0	1	1	0	0	0	1	1
1	1	1	0	1	0	1	0	1
0	0	0	0	1	1	0	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	1	1	0	1	1
1	1	1	1	1	0	1	0	0
1	1	1	0	0	1	0	0	1
0	0	0	0	0	0	0	0	1
1	1	0	0	1	0	1	0	1
0	1	0	0	0	0	0	0	1
1	1	1	0	1	0	1	0	1
0	0	0	1	0	0	1	1	1
1	1	1	1	1	0	1	1	1
0	0	0	0	0	1	1	1	1
0	1	0	1	0	1	0	1	1
0	0	0	0	0	1	0	1	1
0	0	0	0	0	1	0	1	1
1	1	1	1	1	0	1	0	1
0	0	0	1	0	0	0	0	1
0	0	0	1	1	0	1	0	1
0	0	0	1	1	0	1	1	1
1	1	1	0	1	0	0	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	0	0	1	0	1
1	1	0	0	1	0	1	1	1
1	1	1	0	0	0	1	0	1
1	0	1	0	1	1	0	0	0
1	1	0	0	0	0	1	0	1
1	1	1	0	1	0	1	0	1
0	0	1	1	1	0	0	1	1
0	1	0	0	0	0	1	1	1
1	1	0	0	1	0	1	0	0
1	1	1	1	1	0	1	0	1
1	0	1	1	1	0	0	1	1"

Sample information for the second part:"Pleural fluid biochemistry_ADA", "Pleural fluid biochemistry_Total protein", 
"Blood cell analysis_Lymphocyte count", "Pleural fluid biochemistry_Albumin", 
"Blood cell analysis_Neutrophil percentage", "Blood cell analysis_Monocyte percentage", 
"Blood cell analysis_Neutrophil count", "Age" correspond to the values of {values}.
The conclusion is formatted as '结论: [结核性胸腔积液/非结核性胸腔积液][可能性(0-100%)] ([description]),' based on the overall evaluation of key features, providing a clear and concise conclusion. On a new line after the conclusion: '[结核性胸腔积液/非结核性胸腔积液][可能性(0-100%)] ', reflecting the malignancy degree in a format suitable for spreadsheet extraction (table). All responses are delivered in Chinese.
        """

    prompt_English=f"""
    As a respiratory disease expert specializing in the diagnosis and treatment of tuberculous pleural effusion, please analyze the data from the first part related to laboratory tests and clinical features of tuberculous pleural effusion that I uploaded. In this data, the GROUP column indicates 0 for non-tuberculous pleural effusion and 1 for tuberculous pleural effusion. If you can recognize this, please respond with "yes" and make a prediction about whether the data in the second part is indicative of tuberculous pleural effusion. Here is the data from the first part::"
GROUP	Pleural fluid biochemistry_ADA	Pleural fluid biochemistry_Total protein	Blood cell analysis_Lymphocyte count	Pleural fluid biochemistry_Albumin	Blood cell analysis_Neutrophil percentage	Blood cell analysis_Monocyte percentage	Blood cell analysis_Neutrophil count	Age
0	0	1	1	1	0	1	0	1
1	1	1	0	1	0	1	0	1
0	1	1	1	1	1	0	1	1
0	0	0	0	0	0	0	1	1
1	0	0	1	1	0	0	0	0
1	1	0	0	1	0	1	0	1
1	1	1	0	1	0	1	0	1
0	0	0	0	1	1	0	1	1
1	1	0	0	1	0	1	0	1
1	1	1	0	1	0	1	0	0
1	1	1	0	1	0	1	0	0
1	1	1	0	1	0	1	0	0
0	0	1	0	1	0	1	0	1
1	1	1	1	1	0	0	1	0
1	1	1	0	1	1	1	1	1
1	0	0	0	0	1	1	1	1
1	1	1	0	0	0	1	0	1
0	0	0	0	0	0	1	0	1
0	0	1	1	1	0	0	1	1
0	0	0	0	0	1	0	1	1
0	0	1	1	1	0	0	1	1
1	1	1	0	1	0	1	0	0
0	1	0	0	0	0	1	1	1
1	1	1	1	1	0	1	1	1
0	0	0	1	0	0	1	1	1
1	1	0	0	0	0	0	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	1	0	1	0	1
0	0	1	1	1	0	0	1	1
1	1	1	0	1	0	1	0	1
1	0	1	0	1	0	1	1	1
0	0	1	1	1	0	1	1	1
1	1	0	1	1	0	1	0	1
0	0	1	0	1	1	0	0	1
0	1	1	0	0	0	0	0	1
1	1	1	1	1	0	1	1	1
0	0	0	0	1	0	1	1	1
1	1	1	1	1	0	1	0	0
0	0	0	1	1	0	1	0	1
0	1	0	1	1	0	1	1	1
0	0	0	1	0	1	1	1	1
1	1	1	0	1	0	1	0	0
1	1	1	1	1	0	0	0	1
1	1	1	0	1	0	1	0	0
1	1	1	0	0	0	1	0	1
1	1	1	0	1	0	1	0	1
0	0	1	1	1	0	1	0	1
1	1	1	0	1	0	1	0	0
0	0	0	1	1	0	1	1	1
1	1	1	1	1	0	0	1	1
1	1	1	0	1	1	1	1	0
0	0	0	1	1	0	1	1	1
0	0	1	0	1	1	0	1	0
1	1	1	0	0	0	1	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	1	0	1	1	1
1	0	1	1	1	0	1	0	1
1	0	0	0	1	0	1	0	1
1	0	1	1	1	0	1	1	1
1	1	0	0	1	0	1	0	1
1	1	1	0	1	0	1	0	0
0	0	1	1	1	0	1	1	1
1	1	1	0	1	0	1	0	0
1	0	0	0	0	0	1	0	1
0	1	0	0	0	1	1	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	1	1	0	1	1
1	1	1	0	1	0	1	0	1
1	1	0	0	0	0	1	1	1
1	1	0	0	1	1	0	1	1
1	1	0	0	0	0	1	0	1
1	1	0	0	1	0	1	0	0
0	1	1	0	0	1	0	1	1
1	1	1	0	1	0	1	0	1
1	0	0	0	0	0	1	0	1
0	0	0	1	1	0	0	0	1
1	1	0	0	1	0	1	0	1
0	0	0	1	1	0	0	0	1
1	1	1	0	1	0	1	0	1
0	0	0	0	1	0	0	0	1
0	0	1	1	0	0	0	1	1
1	1	1	0	1	0	1	0	1
0	0	0	0	1	1	0	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	1	1	0	1	1
1	1	1	1	1	0	1	0	0
1	1	1	0	0	1	0	0	1
0	0	0	0	0	0	0	0	1
1	1	0	0	1	0	1	0	1
0	1	0	0	0	0	0	0	1
1	1	1	0	1	0	1	0	1
0	0	0	1	0	0	1	1	1
1	1	1	1	1	0	1	1	1
0	0	0	0	0	1	1	1	1
0	1	0	1	0	1	0	1	1
0	0	0	0	0	1	0	1	1
0	0	0	0	0	1	0	1	1
1	1	1	1	1	0	1	0	1
0	0	0	1	0	0	0	0	1
0	0	0	1	1	0	1	0	1
0	0	0	1	1	0	1	1	1
1	1	1	0	1	0	0	0	1
1	1	1	0	1	0	1	0	1
1	1	1	0	0	0	1	0	1
1	1	0	0	1	0	1	1	1
1	1	1	0	0	0	1	0	1
1	0	1	0	1	1	0	0	0
1	1	0	0	0	0	1	0	1
1	1	1	0	1	0	1	0	1
0	0	1	1	1	0	0	1	1
0	1	0	0	0	0	1	1	1
1	1	0	0	1	0	1	0	0
1	1	1	1	1	0	1	0	1
1	0	1	1	1	0	0	1	1"

Sample information for the second part:"Pleural fluid biochemistry_ADA", "Pleural fluid biochemistry_Total protein", 
"Blood cell analysis_Lymphocyte count", "Pleural fluid biochemistry_Albumin", 
"Blood cell analysis_Neutrophil percentage", "Blood cell analysis_Monocyte percentage", 
"Blood cell analysis_Neutrophil count", "Age" correspond to the values of {values}.
The conclusion is formatted as 'CONCLUSION: [Tuberculous pleural effusion/nontuberculous pleural effusion] [Likelihood (0-100%)] ([description]),' based on the overall evaluation of key features, providing a clear and concise conclusion. On a new line after the conclusion: 'CONCLUSION: [Tuberculous pleural effusion/nontuberculous pleural effusion] [Likelihood (0-100%)]', reflecting the malignancy degree in a format suitable for spreadsheet extraction (table). All responses are delivered in English.
        """
    
    # 设置API key
    client = OpenAI(base_url=base_url, api_key=api_key)

    # 根据语言选择不同的 prompt
    if language == "English":
        prompt =   prompt_English# 替换为实际的英文 prompt
    elif language == "Chinese":
        prompt =   prompt_Chinese  # 替换为实际的中文 prompt
    else:
        raise ValueError("Unsupported language. Please choose 'English' or 'Chinese'.")

    # 调用 GPT 模型
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ]
            }
        ],
        model="gpt-4",  # 可以切换为 "gpt-3.5-turbo" 模型
        temperature=0.4  # 控制生成文本的随机性
    )

    # 输出生成的结果
    print(chat_completion.choices[0].message.content)
    return((chat_completion.choices[0].message.content))
