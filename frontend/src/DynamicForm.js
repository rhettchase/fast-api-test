import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Form from '@rjsf/core';
import {
  fetchFormConfig,
  submitUserResponse,
  setUserResponse,
  fetchNextQuestion,
} from './formSlice';
import validator from '@rjsf/validator-ajv8';

function DynamicForm() {
  const dispatch = useDispatch();
  const { currentFormId, formConfig, message, userResponse } = useSelector(
    (state) => state.form
  );

  useEffect(() => {
    if (!formConfig) {
      dispatch(fetchFormConfig(currentFormId));
    }
  }, [currentFormId, dispatch, formConfig]);

  const handleSubmit = ({ formData }) => {
    const questionId = parseInt(
      Object.keys(formData)[0].replace('question', '')
    ); // Extract integer ID
    const response = formData[`question${questionId}`]; // Access using template literal
    const payload = {
      question_id: questionId,
      response: response,
    };

    console.log('Submitting payload:', payload); // Log the payload for debugging
    dispatch(setUserResponse(payload)); // Set user response
    dispatch(submitUserResponse(payload)).then(() => {
      dispatch(fetchNextQuestion(payload)); // Fetch the next question based on the response
    });
  };

  if (message) {
    return <div>{message}</div>;
  }

  if (!formConfig || !formConfig.fields) {
    return <div>Loading...</div>;
  }

  const schema = {
    title: formConfig.title,
    type: 'object',
    properties: formConfig.fields.reduce((acc, field) => {
      acc[field.name] = {
        type: field.type,
        title: field.label,
        enum: field.options,
      };
      return acc;
    }, {}),
  };

  return <Form schema={schema} onSubmit={handleSubmit} validator={validator} />;
}

export default DynamicForm;
