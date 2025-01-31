import { useState } from 'react';
import { UUID } from 'crypto';

import { Button, Group, Paper, Stepper, Text, Textarea } from '@mantine/core';
import { hasLength, useForm } from '@mantine/form';

import { sendFeedback } from '@emoji-search/shared/api/feedback';

import { FirstStep, FirstStepProps } from './FirstStep';

export interface FeedbackFormProps extends Pick<FirstStepProps, 'suggestedEmoji'> {
  searchUid?: UUID;
}

export const FeedbackForm = ({ suggestedEmoji, searchUid }: FeedbackFormProps) => {
  const [activeStep, setActiveStep] = useState(0);
  const [relevantEmoji, setRelevantEmoji] = useState<string>('');
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      rationale: '',
    },
    validate: {
      rationale: hasLength({ min: 1, max: 511 }, 'Rationale must be between 1 and 511 characters'),
    },
  });

  const nextStep = () => setActiveStep((current) => (current < 2 ? current + 1 : current));
  const prevStep = () => setActiveStep((current) => (current > 0 ? current - 1 : current));

  const nextButton = (activeStep: number) => {
    switch (activeStep) {
      case 0:
        return (
          <Button w={80} onClick={nextStep} disabled={relevantEmoji === ''}>
            Next
          </Button>
        );
      case 1:
        return (
          <Button
            w={80}
            color="green"
            onClick={() => {
              if (!form.validate().hasErrors) {
                nextStep();
                sendFeedback({
                  emoji: relevantEmoji.split(' ')[0],
                  searchUid: searchUid!,
                  rationale: form.getValues().rationale,
                });
              }
            }}
          >
            Send
          </Button>
        );
      default:
        return null;
    }
  };

  return (
    <Paper>
      <Stepper active={activeStep}>
        <Stepper.Step label="First step" description="Choose the most relevant emoji">
          <FirstStep
            suggestedEmoji={suggestedEmoji}
            value={relevantEmoji}
            onChange={setRelevantEmoji}
          />
        </Stepper.Step>
        <Stepper.Step label="Second step" description="Justify your choice">
          <Textarea
            withAsterisk
            label={`Write why you think ${relevantEmoji.split(' ')[0]} is most relevant`}
            placeholder="Rationale"
            autosize
            minRows={4}
            maxRows={4}
            key={form.key('rationale')}
            {...form.getInputProps('rationale')}
          />
        </Stepper.Step>
        <Stepper.Completed>
          <Text py="md">🎉 Thank you for helping to improve the project!</Text>
        </Stepper.Completed>
      </Stepper>
      <Group justify="right" mt="md">
        {activeStep < 2 && (
          <Button w={80} variant="default" onClick={prevStep}>
            Back
          </Button>
        )}
        {nextButton(activeStep)}
      </Group>
    </Paper>
  );
};
