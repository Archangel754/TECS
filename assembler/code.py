
def code(mnemonic,mtype):
    # returns binary version of assembly mnemonic of type mtype
    jump = {'null':'000',
                'JGT':'001',
                'JEQ':'010',
                'JGE':'011',
                'JLT':'100',
                'JNE':'101',
                'JLE':'110',
                'JMP':'111'
                }
    dest = {'null':'000',
                'M':'001',
                'D':'010',
                'MD':'011',
                'A':'100',
                'AM':'101',
                'AD':'110',
                'AMD':'111'}
    comp = {'0':'101010',
                '1':'111111',
                '-1':'111010',
                'D':'001100',
                'A':'110000',
                '!D':'001101',
                '!A':'110001',
                '-D':'001111',
                '-A':'110011',
                'D+1':'011111',
                'A+1':'110111',
                'D-1':'001110',
                'A-1':'110010',
                'D+A':'000010',
                'D-A':'010011',
                'A-D':'000111',
                'D&A':'000000',
                'D|A':'010101'
        }
    if mtype == 'comp':
        if 'M' in mnemonic:
            a = '1'
            mnemonic = mnemonic.replace('M','A')
        else:
            a = '0'
        return a + comp[mnemonic]
    elif mtype == 'jump':
        return jump[mnemonic]
    elif mtype == 'dest':
        return dest[mnemonic]
    else:
        raise ValueError('no mtype provided in for assembly code.')
