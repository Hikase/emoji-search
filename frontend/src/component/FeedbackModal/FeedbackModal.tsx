import { Affix, Button, Modal, ScrollArea } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';

import { FeedbackForm, FeedbackFormProps } from './FeedbackForm';

export const FeedbackModal = (props: FeedbackFormProps) => {
  const [opened, { open, close }] = useDisclosure(false);
  return (
    <>
      <Modal
        opened={opened}
        onClose={close}
        title="Send Feedback"
        size="lg"
        centered
        scrollAreaComponent={ScrollArea.Autosize}
      >
        <FeedbackForm {...props} />
      </Modal>
      {props.searchUid && (
        <Affix position={{ bottom: 40, right: 40 }}>
          <Button onClick={open} radius="xl">
            Rate search
          </Button>
        </Affix>
      )}
    </>
  );
};
