import { IExecuteFunctions } from 'n8n-core';
import { INodeExecutionData, INodeType, INodeTypeDescription } from 'n8n-workflow';
import { execSync } from 'child_process';
import { writeFileSync, readFileSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

export class AeMindNode implements INodeType {
    // AETH: definícia n8n uzla pre volanie introspektívneho parsera
    description: INodeTypeDescription = {
        displayName: 'AE Mind Parser',
        name: 'aeMindParser',
        group: ['transform'],
        version: 1,
        description: 'Execute the AE Mind introspective parser pipeline.',
        defaults: {
            name: 'AE Mind Parser',
            color: '#00AAFF',
        },
        inputs: ['main'],
        outputs: ['main'],
        properties: [
            {
                displayName: 'Text',
                name: 'text',
                type: 'string',
                default: '',
            },
        ],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        const text = this.getNodeParameter('text', 0) as string;
        const inputPath = join(tmpdir(), 'ae_mind_input.txt');
        writeFileSync(inputPath, text, 'utf8');
        const outputPath = join(tmpdir(), 'ae_mind_output');
        // AETH: spustenie Python pipeline cez child_process
        execSync(`python -m ae_mind.src.introspective_parser.run_pipeline ${inputPath} --out ${outputPath}.md`);
        const json = readFileSync(`${outputPath}.json`, 'utf8');
        const data = JSON.parse(json);
        return [this.helpers.returnJsonArray([data])];
    }
}
